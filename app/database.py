from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb://medhir:medhir@192.168.0.200:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8")

# Use the 'attendance' database (it will be created automatically if not exists)
db = client["attendance"]

# Use the 'users' collection (it will be created automatically when a document is inserted)
users_col = db["users"]
