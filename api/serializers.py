from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    ProductVariant,
    Order,
    OrderItem,
)

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = ["_id", "username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    display_name = serializers.CharField(
        source="get_name_display",
        read_only=True
    )

    class Meta:
        model = Category
        fields = [
            "_id",
            "name",
            "display_name",
        ]

class SubCategorySerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    display_name = serializers.CharField(
        source="get_name_display",
        read_only=True
    )

    class Meta:
        model = SubCategory
        fields = [
            "_id",
            "category",
            "name",
            "display_name",
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = ProductImage
        fields = [
            "_id",
            "image",
        ]

class ProductVariantSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "_id",
            "size",
            "price",
            "inventory",
        ]

class ProductSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True
    )
    category = serializers.CharField(
        source="sub_category.category.name",
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "_id",
            "name",
            "description",
            "sub_category",
            "category",
            "in_stock",
            "images",
            "variants",
            "createdAt",
        ]

    
class OrderItemSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "_id",
            "product",
            "variant",
            "quantity",
            "unit_price",
        ]

class OrderSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    user = UserSerializer(read_only=True)

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "_id",
            "user",
            "customer_name",
            "customer_email",
            "customer_phone",
            "delivery_address",
            "payment_method",
            "payment_status",
            "is_confirmed",
            "total_price",
            "items",
            "createdAt",
        ]

class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    variant = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=3)


class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    delivery_address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=["cod", "online"])
    items = OrderItemCreateSerializer(many=True)
