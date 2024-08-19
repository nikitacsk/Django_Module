from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_clicked = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def total_price(self):
        return self.quantity * self.product.price


class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    requested_at = models.DateTimeField(auto_now_add=True)

    def is_returnable(self):
        return (timezone.now() - self.order.ordered_at).total_seconds() < 180

    def __str__(self):
        return f"Return for Order #{self.order.id}"
