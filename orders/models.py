from django.db import models
from django.utils import timezone
from clients.models import Client
from products.models import Product
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    # Payment status choices
    PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('partial', 'Partial'),
    ('paid', 'Paid'),
]

    payment_status = models.CharField(
    max_length=20,
    choices=PAYMENT_STATUS_CHOICES,
    default='pending'
)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        return self.quantity * self.price


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)

    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.amount}"