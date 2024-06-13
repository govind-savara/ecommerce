from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from product_app.models import review_collection

# Create your views here.


@api_view(["GET"])
def get_product_popularity_details(request):
    if request.method == "GET":
        pipeline = [
            {
                "$group": {
                    "_id": "$product_id",
                    "average_rating": {"$avg": "$rating"}
                }
            },
            {
                "$sort": {
                    "average_rating": -1
                }
            },
            {
                "$lookup": {
                    "from": "products",
                    "localField": "_id",
                    "foreignField": "product_id",
                    "as": "product_data"
                }
            },
            {
                "$unwind": {
                    "path": "$product_data"
                }
            },
            {
                "$project": {
                    "average_rating": 1,
                    "product_id": "$product_data.product_id",
                    "name": "$product_data.name",
                    "description": "$product_data.description",
                    "price": "$product_data.price",
                    "stock": "$product_data.stock",
                    "category": "$product_data.category",
                }
            }
        ]

        result = review_collection.aggregate(pipeline)
        return Response(list(result))