from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd
import json
import os
import time

# Load the environment variables from the .env file
load_dotenv()

DATABASE_NAME = "SuzukaCircuit"
# COLLECTION_NAME = "reference_telemetries"

MODEL = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.8)

SYSTEM_MESSAGE = """
You are an expert driving coach with extensive experience in analyzing racing telemetry data and providing strategic guidance for track performance optimization. You specialize in reviewing detailed telemetry inputs such as speed, acceleration, braking, throttle position, gear shifts, and cornering lines, and comparing them to ideal track performance metrics.

Your role is to evaluate telemetry data, identify areas where the driver can improve, and make actionable suggestions. You should:

1. Analyze how current driving performance aligns with or deviates from ideal driving techniques and track-specific strategies.
2. Identify specific sections of the track where time can be gained or techniques improved, such as braking points, corner exits, throttle control, or gear usage.
3. Use simple, clear explanations for your feedback, accompanied by analogies when needed, to ensure the driver understands the recommended changes.
4. Provide context by relating specific driving metrics to their real-world impact on lap times and overall performance.
5. Maintain a constructive, insightful, and motivating tone that encourages growth and confidence in the driver's abilities.

Always consider consistency, and efficiency in your recommendations, aiming to help the driver achieve smoother, faster laps around the track.
"""

def retrieve_segment_data(collection_name):
    # Connect to database
    client = MongoClient(os.getenv("MONGODB_CONNECTION_URI"))

    db = client[DATABASE_NAME]
    collection = db[collection_name]

    print('Connected to database')

    # Get maximum segment from data
    max_segment_doc  = collection.find().sort("lapInfo.segment", -1).limit(1)
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

        # Get array of average speeds caclculated for each eub segment
        avg_speed_array = data['speed'].rolling(window=window_size).mean()[window_size-1::window_size].reset_index(drop=True)

        # Convert averaged data into a string for prompt formatting
        avg_speed_str = ', '.join([f"{val:.2f}" for val in avg_speed_array])

        seg_obj = {}
        seg_obj['avg_speeds'] = avg_speed_str
        # add other telem data to obj like above

        # Add all curret segment data to an object 
        data_out['segments'][seg_num] = seg_obj

        # print(f'Retrieved {data_len} documents for segment {seg_num}')
        # print(f'Average speeds: {avg_speed_str}\n')

    # Close the connection after use
    client.close()

    print('Disconnected from database on chain!')

    return data_out
    
def create_prompt(baseline_data, new_data):
    prompt_template = """
    You are an expert driving coach analyzing telemetry data for a driver on the track {track_name}. At the end of this prompt, there are two sets of detailed telemetry data segmented for analysis. For each segment, you will: 
    1. Provide a performance rating out of 10 for the segment based on how the driver telemetry data compares to the baseline telemetry data. 
    2. Write a natural language assessment, limited to 50 words, summarizing the driver's performance in each segment, highlighting strengths, weaknesses, and potential improvements. 

    Please maintain the structure provided: 
    <start of structure example>
    # Track Name: {track_name}

    ## Segment <replace with segment number> 
    - **Performance Rating (out of 10)**: 
    - **Assessment**: 

    ## Segment <replace with next segment number>
    - **Performance Rating (out of 10)**: 
    - **Assessment**: 
    <end of structure example>

    Continue with this format for each segment. Ensure that the response maintains a consistent and structured approach. Be specific and actionable in the assessments, identifying key changes that could lead to improved performance. Here is the data you will be analyzing:

    Baseline Telemetry Data:
    {baseline_data}

    Driver Telemetry Data:
    {new_data}

    """

    # Initialize PromptTemplate for LangChain
    prompt = PromptTemplate(
        input_variables=["baseline_data", "new_data", "track_name"],
        template=prompt_template
    )

    return prompt.format(baseline_data=baseline_data, new_data=new_data, track_name=DATABASE_NAME)

def prompt_llm(user_prompt):
    response = MODEL.invoke([SystemMessage(content=SYSTEM_MESSAGE),HumanMessage(content=user_prompt)])

    return response.content

def main():
    start = time.time()

    reference_telemetry = retrieve_segment_data(collection_name='reference_telemetries')
    player_telemetry = retrieve_segment_data(collection_name='telemetries')

    # print(f'reference_telemetry:\n{json.dumps(reference_telemetry, indent=2)}\n')
    # print(f'player_telemetry:\n{json.dumps(player_telemetry, indent=2)}\n')

    formatted_prompt = create_prompt(reference_telemetry, player_telemetry)

    llm_repsonse = prompt_llm(formatted_prompt)

    llm_output_path = "llm_assessment.md"

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
