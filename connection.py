import streamlit as st
import pymongo
import pandas as pd
import os
from dotenv import load_dotenv
#loads the .env file
load_dotenv(dotenv_path='.env')
uri = os.getenv("MONGO_URI")

if not uri:
    st.error("Error: MONGO_URI is missing from .env file!")
    st.stop()
#forconnectingthewebsitetothecloud
@st.cache_resource
def init_connection():
    #allowing even if internet is blocking it
    return pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)

client = init_connection()
db = client["store_db"]
collection = db["inventory"]

st.title("📦 Store Inventory System")

# CREATERUD
with st.expander("Add New Product"):
    with st.form("add_form"):
        name = st.text_input("Product Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.5)
        if st.form_submit_button("Add to Inventory"):
            collection.insert_one({"name": name, "quantity": qty, "price": price})
            st.success("Added!")
            st.rerun() #so it automates updating the website

# CRUPDATED
with st.expander("Update Product"):
    items_list = list(collection.find())
    if items_list:
        target_name = st.selectbox("Select product to update:", [i['name'] for i in items_list])
        target_item = collection.find_one({"name": target_name})
        
        with st.form("update_form"):
            new_qty = st.number_input("New Quantity", value=target_item['quantity'], min_value=0)
            new_price = st.number_input("New Price", value=target_item['price'], min_value=0.0)
            if st.form_submit_button("Update Product"):
                collection.update_one({"name": target_name}, {"$set": {"quantity": new_qty, "price": new_price}})
                st.success(f"Updated {target_name}!")
                st.rerun() #so it automates updating the website
    else:
        st.write("No items to update.")

# CREADUD
st.subheader("Current Stock")
items = list(collection.find({}, {"_id": 0}))
if items:
    st.table(pd.DataFrame(items))
else:
    st.write("Inventory is empty.")

# CRUDELETE
st.subheader("🛒 Process Sale")
items_list = list(collection.find())

if items_list:
    selected_name = st.selectbox("Select product to sell:", [i['name'] for i in items_list])
    current_item = collection.find_one({"name": selected_name})
    
   
    if current_item:
        remove_qty = st.number_input("Quantity to remove:", min_value=1, max_value=current_item.get('quantity', 0), step=1)
        
        if st.button("Confirm Sale"):
            new_qty = current_item.get('quantity', 0) - remove_qty
            
            if new_qty <= 0:
                
                collection.delete_one({"name": selected_name})
                st.warning(f"Quantity reached 0. {selected_name} has been removed from inventory.")
            else:
                
                collection.update_one({"name": selected_name}, {"$set": {"quantity": new_qty}})
                st.success(f"Sold {remove_qty} units of {selected_name}!")
            
            st.rerun() #so it automates updating the website
else:
    st.write("Inventory is empty.")

# youfindthingymajig
st.subheader("Search Inventory")
search = st.text_input("Enter product name to search")
if search:
    found_item = collection.find_one({"name": {"$regex": search, "$options": "i"}}) #regex for like searching up things without the full name and i for the thingy to be not case sensitive
    if found_item:
        st.write(f"Found: {found_item['name']} | Qty: {found_item['quantity']} | Price: ${found_item['price']}")
    else:
        st.write("Item not found.")


st.subheader("Inventory Summary") #uhh extra for 4/4:)

total_qty = sum(item['quantity'] for item in items)
total_value = sum(item['quantity'] * item['price'] for item in items)

st.write(f"Total items in stock: {total_qty}")
st.write(f"Total inventory value: ${total_value}")