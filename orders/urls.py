from django.urls import path
from .views import invoice_view

urlpatterns = [
    path('invoice/<int:order_id>/', invoice_view, name='invoice'),
]