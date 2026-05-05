from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Order
from .utils import generate_invoice


def invoice_view(request, order_id):
    order = Order.objects.get(id=order_id)

    pdf = generate_invoice(order)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    return response