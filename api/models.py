from django.db import models
from django.contrib.auth.models import User

#category

class Category(models.Model):

    CATEGORY_CHOICES = [
        ("dresses", "Dresses"),
        ("abayas", "Abayas"),
        ("jalabya", "Jalabya"),
    ]

    name = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.get_name_display()

#sub category

class SubCategory(models.Model):

    SUBCATEGORY_CHOICES = [
        ("new", "New Collection"),
        ("ramadan", "Ramadan Collection"),
        ("eid_fitr", "Eid AlFitr Collection"),
        ("winter", "Winter Collection"),
        ("eid_adha", "Eid AlAdha Collection"),
        ("sale", "Sale")
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(
        max_length=100,
        choices=SUBCATEGORY_CHOICES
    )

    def __str__(self):
        return self.get_name_display()

#product 

class Product(models.Model):
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    in_stock = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#product image (upload)

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/",
        max_length=255
    )

    def __str__(self):
        return f"{self.product.name} image"

#product size 

class ProductVariant(models.Model):

    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    size = models.CharField(
        max_length=1,
        choices=SIZE_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "size"],
                name="unique_product_size"
            )
        ]


    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()}"

#Orders

class Order(models.Model):

   

    PAYMENT_METHOD_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("online", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)
    delivery_address = models.TextField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    is_confirmed = models.BooleanField(default=False)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

# Order Item

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    def __str__(self):
        return f"{self.product.name} - {self.variant.get_size_display()} x {self.quantity}"
