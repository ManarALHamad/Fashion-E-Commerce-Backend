from django.urls import path
from . import views


urlpatterns = [

    path("auth/sign-up", views.sign_up, name="sign-up"),
    path("auth/sign-in", views.sign_in, name="sign-in"),
    path("users", views.user_list, name="user-list"),
    path("categories", views.category_list),
    path("subcategories", views.subcategory_list),
    path("products", views.product_list_create),
    path("products/<int:product_id>/images", views.product_image_create),
    path("products/<int:product_id>", views.product_detail),
    path("products/<int:product_id>", views.product_detail),
    path("products/<int:product_id>/variants", views.product_variant_create),
    path("products/<int:product_id>/variants/<int:variant_id>", views.product_variant_detail),
    path("orders", views.order_create, name="order-create"),
    path("orders/mine", views.order_list_mine, name="order-list-mine"),
    path("orders/all", views.order_list_all, name="order-list-all"),
    path("orders/<int:order_id>", views.order_delete, name="order-delete"),



]
