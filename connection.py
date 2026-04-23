import streamlit as st
import pymongo
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Load variables from the .env file
load_dotenv()

# 2. Get the URI from your .env file
# Ensure the key in .env matches "MONGO_URI"
# TEMPORARY TEST: Delete this after you verify it works
uri = "mongodb+srv://dtberpiluadbuser:theguywho@cluster0.1majges.mongodb.net/?retryWrites=true&w=majority"

# 3. Setup Connection (Cached)
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(uri)

client = init_connection()
db = client["store_db"]
collection = db["inventory"]

# 4. App UI
st.title("📦 Store Inventory System")

# Add New Item
with st.expander("Add New Product"):
    with st.form("add_form"):
        name = st.text_input("Product Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.5)
        submit = st.form_submit_button("Add to Inventory")
        
        if submit:
            if name:
                collection.insert_one({"name": name, "quantity": qty, "price": price})
                st.success(f"Added {name} to inventory!")
            else:
                st.error("Please enter a product name.")

# View Inventory
st.subheader("Current Stock")
items = list(collection.find({}, {"_id": 0}))

if items:
    df = pd.DataFrame(items)
    st.table(df)
else:
    st.write("Inventory is empty.")

# Search/Filter
st.subheader("Search Inventory")
search = st.text_input("Enter product name to search")
if search:
    found_item = collection.find_one({"name": {"$regex": search, "$options": "i"}})
    if found_item:
        st.write(f"Found: {found_item['name']} | Qty: {found_item['quantity']} | Price: ${found_item['price']}")
    else:
        st.write("Item not found.")

# Delete
st.subheader("🛒 Process Sale (Remove Stock)")
items = list(collection.find())
item_names = [i['name'] for i in items]

if item_names:
    selected_name = st.selectbox("Select product to remove:", item_names)
    # Find the current item data
    current_item = collection.find_one({"name": selected_name})
    current_qty = current_item['quantity']
    
    st.write(f"Current Stock: {current_qty}")
    
    remove_qty = st.number_input("Quantity to remove/sell:", min_value=1, max_value=current_qty, step=1)
    
    if st.button("Confirm Sale"):
        new_qty = current_qty - remove_qty
        collection.update_one({"name": selected_name}, {"$set": {"quantity": new_qty}})
        st.success(f"Sold {remove_qty} units of {selected_name}!")
        st.rerun() # Refresh the page to show new totals
else:
    st.write("Inventory is empty.")