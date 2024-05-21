from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user_app.models import User
from utility.common_utils import parse_mongo_json
from .models import (
    product_collection, get_default_product_dict, get_updated_product_data,
    review_collection, get_default_review_dict
)

# Create your views here.


class ProductList(APIView):
    """
    List all products, or create a new product.
    """

    def get(self, request):
        products_data = product_collection.find({})
        return Response(parse_mongo_json(list(products_data)))

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


class ReviewList(APIView):
    """
    List all Review data or create a new review of product
    """
    def get(self, request):
        query = {}

        if "product_id" in request.data:
            try:
                query["product_id"] = int(request.data["product_id"])
            except Exception as e:
                return Response({"error": "Please provide a valid product id"}, HTTP_400_BAD_REQUEST)

        if "user_id" in request.data:
            try:
                query["user_id"] = int(request.data["user_id"])
            except Exception as e:
                return Response({"error": "Please provide a valid user id"}, HTTP_400_BAD_REQUEST)

        reviews = review_collection.find(query)
        return Response(parse_mongo_json(list(reviews)), HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product id is missing!"}, HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except Exception as e:
            return Response({"error": "Please provide a valid product id"}, HTTP_400_BAD_REQUEST)

        product_data = product_collection.find_one({"product_id": product_id})
        if not product_data:
            return Response({"error": f"Product does not exist with product_id={product_id}"}, HTTP_400_BAD_REQUEST)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User id is missing!"}, HTTP_400_BAD_REQUEST)

        user_data = User.objects.filter(id=user_id).first()
        if not user_data:
            return Response({"error": "User does not exists!"}, HTTP_400_BAD_REQUEST)

        review_data = review_collection.find_one({"product_id": product_id, "user_id": user_data.id})
        if review_data:
            return Response({"error": "Already you reviewed this product."}, HTTP_400_BAD_REQUEST)

        rating = request.data.get("rating")
        if not rating:
            return Response({"error": "Please provide rating between 1 to 5"})

        try:
            rating = int(rating)
        except Exception as e:
            return Response({"error": "Please provide a valid rating between 1 to 5"})

        review_data = get_default_review_dict()
        review_data.update({
            "product_id": product_id,
            "user_id": user_data.id,
            "rating": rating,
        })

        if "comment" in request.data:
            review_data["comment"] = request.data["comment"]

        result = review_collection.insert_one(review_data)
        print(f"review id: {result.inserted_id}")
        return Response({"message": "Review created!"}, HTTP_201_CREATED)


class ReviewDetails(APIView):
    """
    Retrieve, update or delete a review
    """
    def get(self, request, review_id):
        query = {'_id': ObjectId(review_id)}
        review_data = review_collection.find_one(query)
        return Response(parse_mongo_json(review_data))

    def put(self, request, review_id):
        query = {"$_id": ObjectId(review_id)}
        review_data = review_collection.find_one(query)
        if not review_data:
            return Response({"error": f"Review does not exist!"}, HTTP_400_BAD_REQUEST)

        new_data = {}
        if "rating" in request.data:
            try:
                new_data["rating"] = int(request.data["rating"])
            except Exception as e:
                return Response({"error": "Please provide a valid rating between 1 to 5"})

        if "comment" in request.data:
            new_data["comment"] = request.data["comment"]

        if not new_data:
            return Response({"error": "Please provide rating or comment to update"}, HTTP_400_BAD_REQUEST)

        result = review_collection.update_one(query, {"$set": new_data})
        if result.modified_count:
            return Response({"message": "Review details updated!"}, HTTP_200_OK)
        else:
            return Response({"error": "Unable to update review details!"}, HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        query = {"_id": ObjectId(review_id)}
        result = review_collection.delete_one(query)
        if result.deleted_count:
            return Response({"message": "Review deleted!"}, HTTP_200_OK)
        else:
            return Response({"error": "Unable to delete review!"}, HTTP_400_BAD_REQUEST)
