from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import time

def get_database_connection():
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Connect to MongoDB
            client = MongoClient(
                "mongodb://medhir:medhir@192.168.0.200:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8",
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
            # Use the 'attendance' database
            db = client["Attendance-Service"]
            
            # Use the 'users' collection
            users_col = db["Registered-Users"]
            
            return users_col
            
        except ConnectionFailure as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to MongoDB after {max_retries} attempts")
                raise e

# Initialize the collection
users_col = get_database_connection()
