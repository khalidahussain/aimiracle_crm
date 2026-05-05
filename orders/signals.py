from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import OrderItem, Order, Payment
from products.models import Product


# -------------------------------
# 1. AUTO UPDATE ORDER TOTAL
# -------------------------------

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.quantity * item.price for item in order.items.all())
    order.total_amount = total
    order.save(update_fields=['total_amount'])


# -------------------------------
# 2. AUTO UPDATE PAYMENT STATUS
# -------------------------------

@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, **kwargs):
    order = instance.order
    total_paid = sum(p.amount for p in order.payments.all())

    if total_paid >= order.total_amount:
        order.payment_status = 'paid'
    elif total_paid > 0:
        order.payment_status = 'partial'
    else:
        order.payment_status = 'pending'

    order.save(update_fields=['payment_status'])


# -------------------------------
# 3. INVENTORY DEDUCTION ON CONFIRM
# -------------------------------

@receiver(pre_save, sender=Order)
def deduct_stock_on_confirm(sender, instance, **kwargs):
    if not instance.pk:
        return  # new order, skip

    previous = Order.objects.get(pk=instance.pk)

    # only trigger when status changes to confirmed
    if previous.status != 'confirmed' and instance.status == 'confirmed':
        for item in instance.items.all():
            product = item.product

            if product.stock_quantity < item.quantity:
                raise ValueError(f"Not enough stock for {product.name}")

            product.stock_quantity -= item.quantity
            product.save()