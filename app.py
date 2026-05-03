from pymongo import MongoClient


uri = "mongodb+srv://dtberpiluadbuser:fayefaye@cluster0.1majges.mongodb.net/?appName=Cluster0"


client = MongoClient(uri)
db = client["my_database"]
collection = db["my_collection"]


test_data = {"name": "Test User", "message": "Hello from Python!"}
result = collection.insert_one(test_data)

print(f"Success! Document inserted with ID: {result.inserted_id}")
