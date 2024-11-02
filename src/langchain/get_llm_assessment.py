from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import json
import os

# Load the environment variables from the .env file
load_dotenv()


def retrieve_segment_data(segment):
    # Connect to database
    client = MongoClient(os.getenv("MONGODB_CONNECTION_URI"))

    print('Connected to database from chain!')

    # Close the connection after use
    client.close()

    print('Disconnected from database on chain!')
    

def main():
    retrieve_segment_data(1)


if __name__ == "__main__":
    main()
