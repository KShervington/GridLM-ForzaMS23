from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.prompts import PromptTemplate
import pandas as pd
import json
import os

# Load the environment variables from the .env file
load_dotenv()

DATABASE_NAME = "SuzukaCircuit"
# COLLECTION_NAME = "reference_telemetries"

# TODO: Create system prompt to tell the LLM how to behave
# TODO: Create "user" prompt that logically organizes data into segments to be passed to LLM fro comparison and assessment

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
    

def main():
    reference_telemetry = retrieve_segment_data(collection_name='reference_telemetries')
    player_telemetry = retrieve_segment_data(collection_name='telemetries')

    print(f'reference_telemetry:\n{json.dumps(reference_telemetry, indent=2)}\n')
    print(f'player_telemetry:\n{json.dumps(player_telemetry, indent=2)}\n')


if __name__ == "__main__":
    main()
