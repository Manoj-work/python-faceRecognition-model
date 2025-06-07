from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://singhsaurav182001:2nxNgYzqBIMAtSJE@cluster0.ft9op.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Use the 'attendance' database (it will be created automatically if not exists)
db = client["attendance"]

# Use the 'users' collection (it will be created automatically when a document is inserted)
users_col = db["users"]
