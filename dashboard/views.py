from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from orders.models import Order
from clients.models import Client
from products.models import Product


@login_required
def dashboard_view(request):
    user = request.user

    # -----------------------------
    # Role logic
    # -----------------------------
    if user.role == 'admin':
        dashboard_type = 'admin'
    elif user.role == 'sales':
        dashboard_type = 'sales'
    elif user.role == 'trainer':
        dashboard_type = 'trainer'
    else:
        dashboard_type = 'operations'

    # -----------------------------
    # Role-based order filtering
    # -----------------------------
    if user.role == 'admin':
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(created_by=user).order_by('-created_at')

    # -----------------------------
    # Stats (based on filtered data)
    # -----------------------------
    total_orders = orders.count()

    total_revenue = orders.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Shared/global data
    total_clients = Client.objects.count()
    total_products = Product.objects.count()

    # -----------------------------
    # Recent Orders
    # -----------------------------
    recent_orders = orders[:5]

    # -----------------------------
    # Chart Data
    # -----------------------------
    labels = [o.created_at.strftime("%b") for o in orders]
    data = [float(o.total_amount) for o in orders]

    # -----------------------------
    # Low Stock (Admin only)
    # -----------------------------
    if user.role == 'admin':
        low_stock_products = Product.objects.filter(stock_quantity__lte=5)
    else:
        low_stock_products = None

    # -----------------------------
    # Context
    # -----------------------------
    context = {
        'dashboard_type': dashboard_type,
        'total_orders': total_orders,
        'total_clients': total_clients,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'labels': labels,
        'data': data,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'dashboard/index.html', context)