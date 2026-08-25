from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, SubCategory, Product
from .serializers import ( UserSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer)


def create_access_token(user):
    token = RefreshToken.for_user(user).access_token
    token["payload"] = {
        "_id": str(user.id),
        "username": user.username,
    }
    return str(token)

@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    username = request.data.get("username", "").strip()
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "")
    confirm_password = request.data.get("confirmPassword", "")

    if not username:
        return Response(
            {"err": "Username is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not email:
        return Response(
            {"err": "Email is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not password:
        return Response(
            {"err": "Password is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
   
    if password != confirm_password:
        return Response(
            {"err": "Passwords do not match."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"err": "That username is already taken."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {"err": "That email is already registered."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    token = create_access_token(user)

    return Response({"token": token}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"err": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = create_access_token(user)
    return Response({"token": token})

@api_view(["GET"])
def user_list(request):
    users = User.objects.all().order_by("username")
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def product_list_create(request):

    if request.method == "GET":
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
