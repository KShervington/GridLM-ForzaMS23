from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import multiprocessing
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd
import numpy as np
import json
import os
import time
from compare_data import compare_telemetry

# Load the environment variables from the .env file
load_dotenv()

DATABASE_NAME = "SuzukaCircuit"

USE_LOCAL_MODEL = True

if USE_LOCAL_MODEL:
    MODEL = ChatOllama(
    disable_streaming=True,
    temperature=0.5,
    model='llama3.2:3b-instruct_local',
    num_ctx=10000,
    num_gpu=1,
    num_predict=5000,
    num_thread=multiprocessing.cpu_count() / 2, # recommended to use number of physical cores rather than logical
)
else:
    MODEL = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.5)

# System message to be sent to the model
SYSTEM_MESSAGE = """
You are an expert driving coach with extensive experience in analyzing racing telemetry data and providing strategic guidance for track performance optimization. Your role is to evaluate telemetry data, identify areas where the driver can improve, and make actionable suggestions. Always provide clear, specific, and motivating feedback to help the driver achieve smoother and faster laps.
"""

def retrieve_segment_data(collection_name):
    # Connect to database
    client = MongoClient(os.getenv("MONGODB_CONNECTION_URI"))

    db = client[DATABASE_NAME]
    collection = db[collection_name]

    print('Connected to database')

    # Get maximum segment from data
    max_segment_doc = collection.find().sort("lapInfo.segment", -1).limit(1)
    max_segment_num = max_segment_doc[0]["lapInfo"]["segment"]

    data_out = {}

    data_out['segments'] = {}

    for seg_num in range(1,max_segment_num+1):
        # Retrieve data based on segment
        data = pd.DataFrame(list(collection.find({"lapInfo.segment": seg_num})))

        data_len = len(data)

        sub_segments = 10

        # Number of values to be averaged within each subsegment
        window_size = int(data_len / sub_segments)+1

        # Get array of average values caclculated for each sub segment
        avg_speed_array = data['speed'].rolling(window=window_size).mean()[window_size-1::window_size].reset_index(drop=True)
        avg_brake_pressure_array = data['brake'].rolling(window=window_size).mean()[window_size-1::window_size].reset_index(drop=True)
        avg_throttle_percent_array = data['throttlePercent'].rolling(window=window_size).mean()[window_size-1::window_size].reset_index(drop=True)

        # Get the most frequent gear value in each subsegment
        most_common_gear_array = data['gear'].rolling(window=window_size).apply(lambda x: pd.Series(x).value_counts().idxmax(), raw=True)[window_size-1::window_size].reset_index(drop=True)

        # Use numpy for vectorized operations
        x_acceleration_array = np.array([geometry['accelerationX'] for geometry in data['geometry']])
        y_acceleration_array = np.array([geometry['accelerationY'] for geometry in data['geometry']])

        # Calculate true rate of change by combining forward and lateral acceleration
        data['acceleration'] = np.sqrt(x_acceleration_array**2 + y_acceleration_array**2)

        avg_accel_array = data['acceleration'].rolling(window=window_size).mean()[window_size-1::window_size].reset_index(drop=True)

        # Can categorize data based on relation to max and min values

        seg_obj = {}
        seg_obj['avg_speed_over_time'] = avg_speed_array
        seg_obj['avg_acceleration_over_time'] = avg_accel_array
        seg_obj['avg_brake_pressure_over_time'] = avg_brake_pressure_array
        seg_obj['avg_throttle_percentage_over_time'] = avg_throttle_percent_array
        seg_obj['most_common_gear_values_over_time'] = most_common_gear_array

        # Convert values of each attribute in seg_obj into a string for prompt formatting
        # for attr, value in seg_obj.items():
        #     seg_obj[attr] = ', '.join([f"{val:.2f}" for val in value])

        # Add all curret segment data to an object 
        data_out['segments'][seg_num] = seg_obj

    # Close the connection after use
    client.close()

    print('Disconnected from database on chain!')

    return data_out
    
def create_prompt(data_comparisons):
    prompt_template = """
    Below are summarized telemetry data for the track {track_name}, segmented for analysis. Your task is to:
    1. Performance Rating (out of 10): For each segment, rate the driver's performance based on how their telemetry data compares to the baseline data.
    2. Assessment: Write a concise assessment (maximum 50 words) for each segment, highlighting strengths, weaknesses, and potential improvements.
    
    Please follow this structure for your response:
    # Track Name: {track_name} 

    ## Segment <segment number> 
    - **Performance Rating (out of 10)**: 
    - **Assessment**: 

    ## Segment <next segment number> 
    - **Performance Rating (out of 10)**: 
    - **Assessment**: 

    Ensure that your response is consistent and structured. Be specific and actionable in your assessments, identifying key changes that could lead to improved performance. Repeat the above structure for all 10 segments in the data below.

    Comparison of Driver Telemetry Data to the Baseline Telemetry Data:
    {data_comparisons}
    """

    # Initialize PromptTemplate for LangChain
    prompt = PromptTemplate(
        input_variables=["data_comparisons", "track_name"],
        template=prompt_template
    )

    return prompt.format(data_comparisons=data_comparisons, track_name=DATABASE_NAME)

def prompt_llm(user_prompt):
    response = MODEL.invoke([SystemMessage(content=SYSTEM_MESSAGE),HumanMessage(content=user_prompt)])

    return response.content

def main():
    start = time.time()

    reference_telemetry = retrieve_segment_data(collection_name='reference_telemetries')
    # reference_telemetry = json.dumps(reference_telemetry, indent=2)

    player_telemetry = retrieve_segment_data(collection_name='telemetries')
    # player_telemetry = json.dumps(player_telemetry, indent=2)

    # Calculate deltas between reference and player telemetry data
    comparisons = compare_telemetry(baseline_data=reference_telemetry, driver_data=player_telemetry)
    comparisons = json.dumps(comparisons, indent=2)

    formatted_prompt = create_prompt(comparisons)

    print('Initiating LLM assessment...')
    llm_repsonse = prompt_llm(formatted_prompt)

    llm_output_file = f"llm_assessment_0.md"
    llm_output_path = os.path.join(os.getcwd(), "src", "experiments", "llm_outputs", "llama_3-2_3b_instruct", llm_output_file) # Executed from root directory

    try:
        with open(llm_output_path, "w") as f:
            # Write to the file
            f.write(llm_repsonse)

            f.close()

            print(f'Wrote LLM response to local file: {llm_output_path}')
    except:
        print(f"Error writing LLM response to file: {llm_output_path}")

    end = time.time()

    print(f'Took [{end - start}] seconds to execute.')

if __name__ == "__main__":
    main()
