from django.contrib import admin

from taxi_car.models import Address, Feedback


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Адрес"""
    list_display = 'address', 'time_work', 'phone_mtc', 'phone_a1', 'phone_life', 'created', 'updated'

    def has_add_permission(self, request):
        """Создание только одной записи"""
        if Address.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Запретить удаление"""
        return False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Обратная связь"""
    list_display = 'name', '__str__', 'message', 'published', 'created', 'updated'
    list_filter = 'published', 'created', 'updated'
    list_editable = 'published',
    readonly_fields = 'name', 'phone', 'email', 'message', 'published', 'created', 'updated'
    search_fields = 'name', 'phone', 'email'
    search_help_text = 'Поиск по имени, телефону и почте'
    date_hierarchy = 'created'
    list_per_page = 20
