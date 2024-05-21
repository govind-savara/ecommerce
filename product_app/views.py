from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from utility.common_utils import parse_mongo_json
from .models import (
    product_collection, get_default_product_dict, get_updated_product_data,
    review_collection, get_default_review_dict
)

# Create your views here.


class ProductList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request):
        products_data = product_collection.get_records()
        return Response(products_data)

    def post(self, request):
        product_name = request.data.get("name")
        if not product_name:
            return Response({"error": "Please enter product name."})

        try:
            last_record = product_collection.find().sort({"$natural": -1}).limit(1)[0]
            last_product_id = last_record.get("product_id") or 0
        except Exception as e:
            print(f"exception {e}")
            last_product_id = 0
        print(f"last product id: {last_product_id}")

        product_data = get_default_product_dict()
        print(f"product data: {product_data}")
        product_data["product_id"] = last_product_id + 1

        # update the data from request
        product_data = get_updated_product_data(product_data, request.data)
        result = product_collection.insert_one(product_data)
        print(f"result id: {result.inserted_id}")
        print(f"product_data: {product_data}")
        resp_data = parse_mongo_json(product_data)
        return Response(resp_data, HTTP_201_CREATED)

class ProductDetail(APIView):
    """
    Retrieve, update or delete a product element.
    """
    def get(self, request, product_id):
        product_data = product_collection.find_one({"product_id": product_id})
        resp_data = parse_mongo_json(product_data)
        return Response(resp_data, HTTP_200_OK)

    def put(self, request, product_id):
        product_data = product_collection.find_one({"product_id": product_id})
        if not product_data:
            return Response({"error": f"Product does not exist with product_id '{product_id}'"}, HTTP_400_BAD_REQUEST)

        new_data = get_updated_product_data({}, request.data)
        result = product_collection.update_one({"product_id": product_id}, {"$set": new_data})
        if result.modified_count:
            return Response({"message": "Product details updated!"}, HTTP_200_OK)
        else:
            return Response({"error": "Unable to update product details!"}, HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        result = product_collection.delete_one({"product_id": product_id})
        if result.deleted_count:
            return Response({"message": "Product deleted!"}, HTTP_200_OK)
        else:
            return Response({"error": "Unable to delete product!"}, HTTP_400_BAD_REQUEST)
