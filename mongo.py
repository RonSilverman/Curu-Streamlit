import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://msramasubramanya23:LtlHRUrtZcxUPVcf@cluster0.h7ohhbr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def search_products_by_keyword(db_name, collection_name, keyword):
    try:
        # Access the database
        db = client[db_name]
        
        # Access the collection
        collection = db[collection_name]
        
        # Search for products containing the keyword in their title
        products = collection.find({"Product Title": {"$regex": keyword, "$options": "i"}})
        
        results = []
        for product in products:
            # Extract the required details
            product_link = product.get("Product Link", "No link available")
            review_summary = product.get("Review Summary", "No review summary available")
            reviewer_details = product.get("Reviewer Details", "No reviewer details available")
            
            results.append({
                "title": product.get("Product Title", "No title available"),
                "link": product_link,
                "review_summary": review_summary,
                # "reviewer_details": reviewer_details
            })
        
        return results if results else "No products found"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app
st.title("Amazon Product Reviews Search")

keyword = st.text_input("Enter a keyword to search for product titles:")

if keyword:
    result = search_products_by_keyword('Curu-Amazon-Data', 'reviews', keyword)
    
    if isinstance(result, str):
        st.write(result)
    else:
        # Convert results to DataFrame
        df = pd.DataFrame(result)
        st.dataframe(df)