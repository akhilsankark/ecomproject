import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to='category')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to='product')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateField(auto_now_add=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Cart(models.Model):
    cart_id = models.CharField(max_length=300, blank= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username if self.user else 'Guest'}"

    def get_total_price(self):
        return sum(item.prod_sub_total() for item in self.prods.all())

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='prods')
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def prod_sub_total(self):
        return self.product.price * self.quantity


# Object Relational Mapping (ORM)
