from datetime import datetime, timedelta

import jwt

from rest_framework import permissions
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import User
from .serializers import UserSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_signup(request):
    if request.method == "POST":
        user_name = request.data.get("username")
        if not user_name:
            return Response({"error": "Please enter Username!"}, HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user_name).first()
        if user:
            return Response({"error": "Username already exists!"}, HTTP_400_BAD_REQUEST)

        email = request.data.get("email")
        if not email:
            return Response({"error": "Please enter email!"}, HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            return Response({"error": "Email already exists!"}, HTTP_400_BAD_REQUEST)

        password = request.data.get("password")
        if not password:
            return Response({"error": "Please enter password!"}, HTTP_400_BAD_REQUEST)

        request_data = request.data.copy()
        request_data["password"] = make_password(password)

        serializer = UserSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_login(request):
    if request.method == "POST":
        email = request.data.get("email")

        if not request.data.get("password"):
            return Response({"message": "Please enter password!"}, HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"message": "User not found!"}, HTTP_400_BAD_REQUEST)

        if not check_password(request.data["password"], user.password):
            return Response({"message": "Please enter a valid password!"}, HTTP_400_BAD_REQUEST)

        current_time = datetime.utcnow()
        payload = {
            "id": user.id,
            "exp": current_time + timedelta(180),
            "iat": current_time,
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token,
            "user_id": user.id,
            "username": user.username
        }
        return response


@api_view(["GET"])
def loggedin_user(request):
    if request.method == "GET":
        token = request.COOKIES.get("jwt")
        if not token:
            return Response({"message": "Unauthenticated!"}, HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            return Response({"message": "Unauthenticated!"}, HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=payload["id"]).first()
        data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
        return Response(data)


@api_view(["POST"])
def user_logout(request):
    if request.method == "POST":
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "Success"}
        return response
