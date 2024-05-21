import json

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from product_app.models import product_collection
from .models import User, OrderModel, OrderDetails

# Create your views here.


@api_view(["POST"])
def place_order(request):
    if request.method == "POST":
        print(f"request data: {request.data}")

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User id is missing!"}, HTTP_400_BAD_REQUEST)

        user_data = User.objects.filter(id=user_id).first()
        if not user_data:
            return Response({"error": "User does not exists!"}, HTTP_400_BAD_REQUEST)

        total_amount = 0
        discount = 0
        shipping_charge = 0
        # order_data = {
        #     "user_id": user_data.id,
        #     "total_amount": total_amount,
        #     "discount": discount,
        #     "shipping_charge": shipping_charge,
        #     "status": "initiated",
        # }
        order_obj = OrderModel(
            user=user_data,
            total_amount=total_amount,
            shipping_charge=shipping_charge,
            discount=discount,
            status="initiated"
        )
        order_obj.save()
        order_id = order_obj.id

        # product_ids_str = request.data.get("product_ids")
        # product_ids = product_ids_str.split(',')
        # print(f"product_ids: {product_ids}, type: {type(product_ids)}")
        ordered_products = request.data.get("products", {})

        products_details = product_collection.find({"product_id": {"$in": list(map(int, ordered_products.keys()))}})
        # order_details_data = []
        for product_data in products_details:
            product_id = product_data["product_id"]
            product_price = product_data["price"]
            quantity = ordered_products[str(product_id)]["quantity"]
            total_amount += (product_price*quantity)
            order_details_obj = OrderDetails(
                order=order_obj,
                product_id=product_id,
                product_price=product_price,
                quantity=quantity,
            )
            order_details_obj.save()

            rem_quantity = product_data["stock"] - quantity
            # reduce stock quantity in products store
            product_collection.update_one({"product_id": product_id}, {"$set": {"quantity": rem_quantity}})

        if total_amount:
            OrderModel.objects.filter(id=order_id).update(total_amount=total_amount)

        return Response({"message": "Successfully placed order!"})
