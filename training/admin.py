from django.contrib import admin
from .models import TrainingSession


class TrainingSessionAdmin(admin.ModelAdmin):

    list_display = ('client', 'trainer', 'topic', 'session_date', 'status')

    # 🔐 FILTER DATA
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superuser sees all
        if request.user.is_superuser:
            return qs

        # Trainer sees only assigned sessions
        return qs.filter(trainer=request.user)

    # 🔐 AUTO ASSIGN TRAINER
    def save_model(self, request, obj, form, change):
        if not obj.trainer:
            obj.trainer = request.user
        super().save_model(request, obj, form, change)

    # 🔐 RESTRICT EDIT
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is None:
            return True

        return obj.trainer == request.user

    # 🔐 RESTRICT DELETE
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(TrainingSession, TrainingSessionAdmin)