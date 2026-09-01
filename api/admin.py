from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, ProductVariant, Order, OrderItem

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(Order)
admin.site.register(OrderItem)