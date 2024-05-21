import os
from datetime import datetime

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


DB_CONNECTION_STRING = os.getenv("PRODUCT_DB_CONNECTION_STRING")
DB_NAME = os.getenv("PRODUCT_DB_NAME")

# connect to db
my_client = MongoClient(DB_CONNECTION_STRING)
my_db = my_client[DB_NAME]


# db collections
product_collection = my_db["products"]
review_collection = my_db["review"]

def get_default_product_dict():
    """
    This method contains the raw data that must be added in db with default values
    """
    return {
        "product_id": 0,
        "name": "",
        "description": "",
        "price": 0.00,
        "category": "",
        "stock": 0,
        "created_at": datetime.utcnow(),
    }

def get_default_review_dict():
    """
    This method contains the raw data that must be added in db with default values
    """
    return {
        "product_id": 0,
        "user_id": 0,
        "rating": 0,
        "comment": "",
        "created_at": datetime.utcnow(),
    }


def get_updated_product_data(vals, data):
    if "name" in data:
        vals["name"] = data["name"]
    if "description" in data:
        vals["description"] = data["description"]
    if "price" in data:
        try:
            vals["price"] = float(data["price"])
        except Exception as e:
            print(f"Exception in product price: {e}")
    if "category" in data:
        vals["category"] = data["category"]
    if "stock" in data:
        try:
            vals["stock"] = int(data["stock"])
        except Exception as e:
            print(f"Exception in product stock: {e}")

    return vals
