from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'status',
        'payment_status',
        'total_amount',
        'invoice_link',
    )

    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ('created_by',)

    # 🔗 Invoice button
    def invoice_link(self, obj):
        url = reverse('invoice', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">Download</a>',
            url
        )
    invoice_link.short_description = "Invoice"

    # 🔐 Filter orders by user
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.role == 'admin':
            return qs

        return qs.filter(created_by=request.user)

    # 🔐 Auto assign creator
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # 🔐 Restrict editing
    def has_change_permission(self, request, obj=None):
        if request.user.role == 'admin':
            return True

        if obj is None:
            return True

        return obj.created_by == request.user

    # 🔐 Restrict delete
    def has_delete_permission(self, request, obj=None):
        return request.user.role == 'admin'

    # 🔐 Restrict view
    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Order, OrderAdmin)