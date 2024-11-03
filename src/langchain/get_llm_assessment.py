from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import json
import os

# Load the environment variables from the .env file
load_dotenv()

DATABASE_NAME = "test"
COLLECTION_NAME = "telemetries"

def retrieve_segment_data():
    # Connect to database
    client = MongoClient(os.getenv("MONGODB_CONNECTION_URI"))

    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Get maximum segment from data
    max_segment_doc  = collection.find().sort("lapInfo.segment", -1).limit(1)
    max_segment_num = max_segment_doc[0]["lapInfo"]["segment"]

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

        print(f'Retrieved {data_len} documents for segment {seg_num}')
        print(f'Average speeds: {avg_speed_str}\n')

    # Close the connection after use
    client.close()

    print('Disconnected from database on chain!')
    

def main():
    retrieve_segment_data()


if __name__ == "__main__":
    main()
