from pymongo import MongoClient

# Paste your connection string here
uri = "mongodb+srv://dtberpiluadbuser:theguywho@cluster0.1majges.mongodb.net/?appName=Cluster0"

# Connect
client = MongoClient(uri)
db = client["my_database"]
collection = db["my_collection"]

# Try inserting a test document
test_data = {"name": "Test User", "message": "Hello from Python!"}
result = collection.insert_one(test_data)

print(f"Success! Document inserted with ID: {result.inserted_id}")