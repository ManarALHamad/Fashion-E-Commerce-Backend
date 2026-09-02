from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import ( Category, SubCategory, Product, ProductImage)
from .serializers import ( UserSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer, ProductImageSerializer)
from .models import ProductImage
from .serializers import ProductImageSerializer
from .models import ProductVariant
from .serializers import ProductVariantSerializer
from .models import Order, OrderItem, Product, ProductVariant
from .serializers import OrderSerializer, OrderCreateSerializer


def create_access_token(user):
    token = RefreshToken.for_user(user).access_token
    token["payload"] = {
        "_id": str(user.id),
        "username": user.username,
        "email": user.email,
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
    print('inside list_create')

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
    
@api_view(["POST"])
@permission_classes([AllowAny])
def product_image_create(request, product_id):

    try:
        product = Product.objects.get(pk=product_id)

    except Product.DoesNotExist:
        return Response(
            {"err": "Product not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductImageSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(product=product)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def product_detail(request, product_id):

    try:
        product = Product.objects.get(pk=product_id)

    except Product.DoesNotExist:
        return Response(
            {"err": "Product not found."},
            status=status.HTTP_404_NOT_FOUND
        )

   
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    
    if request.method == "PUT":
        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    
    if request.method == "DELETE":
        product.delete()

        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_200_OK
        )



@api_view(["POST"])
@permission_classes([AllowAny])
def product_variant_create(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"err": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductVariantSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([AllowAny])
def product_variant_detail(request, product_id, variant_id):

    try:
        variant = ProductVariant.objects.get(
            pk=variant_id,
            product_id=product_id
        )

    except ProductVariant.DoesNotExist:
        return Response(
            {"err": "Variant not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductVariantSerializer(
        variant,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_create(request):
    serializer  = OrderCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    items_data = data.pop("items")

    total_price = sum(
        item["unit_price"] * item["quantity"] for item in items_data
    )

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        **data
    )

    for item in items_data: 
        OrderItem.objects.create(
            order=order,
            product_id=item["product"],
            variant_id=item["variant"],
            quantity=item["quantity"],
            unit_price=item["unit_price"]

        )


        
    return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list_mine(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return Response(OrderSerializer(orders, many=True).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list_all(request):
    orders = Order.objects.all().order_by("-created_at")
    return Response(OrderSerializer(orders, many=True).data)


#admin can delete orders 

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def order_delete(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    order.delete()

    return Response(
        {"message": "Order deleted successfully."},
        status=status.HTTP_200_OK
    )