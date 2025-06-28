from django.contrib import admin
from django.utils.safestring import mark_safe

from taxi_car.models import Address, Feedback, About, Personnel, CarBrand, Car, Reviews


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
    list_display = 'name', 'phone_email', 'message', 'published', 'created', 'updated'
    list_filter = 'published', 'created', 'updated'
    list_editable = 'published',
    readonly_fields = 'name', 'phone_email', 'message', 'published', 'created', 'updated'
    search_fields = 'name', 'phone_email', 'email'
    search_help_text = 'Поиск по имени, телефону или почте'
    date_hierarchy = 'created'
    list_per_page = 20


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """О нас"""
    list_display = 'numbers', 'name', 'description', 'created', 'updated'
    date_hierarchy = 'created'
    ordering = ['numbers']
    list_per_page = 20


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    """Персонал"""
    fields = 'preview_avatar', 'photo', 'fio', 'position', 'status', 'created', 'updated'
    list_display = 'preview_avatar', 'fio', 'position', 'status', 'created', 'updated'
    list_editable = 'status',
    readonly_fields = 'preview_avatar', 'created', 'updated',
    date_hierarchy = 'created'
    list_per_page = 20

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'


class CarInline(admin.TabularInline):
    """Контроль времени"""
    model = Car
    fields = 'photo', 'car_brand', 'name', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    classes = ['collapse']
    list_per_page = 20
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """Стиль отображения"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
        formset.form.base_fields['year'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['power_reserve'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
        return formset


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    """Бренд автомобиля"""
    list_display = 'name', 'car_count', 'created', 'updated'
    date_hierarchy = 'created'
    inlines = CarInline,
    list_per_page = 20

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'

    def car_count(self, obj):
        """Количество автомобилей этого бренда"""
        return obj.car_set.count()

    car_count.short_description = 'Количество моделей'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    fields = 'preview_avatar', 'photo', 'name', 'message', 'status', 'created', 'updated'
    list_display = 'preview_avatar', 'name', 'message', 'status', 'created', 'updated'
    list_editable = 'status',
    readonly_fields = 'preview_avatar', 'created', 'updated',
    date_hierarchy = 'created'
    list_per_page = 20

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60" style="border-radius: 60px;"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'












# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     """Модель автомобиля"""
#     list_display = '__str__', 'preview_avatar', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
#     fields = 'preview_avatar', 'photo', 'car_brand', 'name', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
#     readonly_fields = 'preview_avatar', 'created', 'updated',
#     list_editable = 'status',
#     list_filter = 'status', 'car_brand__name', 'year',
#     search_fields = 'name', 'car_brand__name', 'year', 'power_reserve'
#     search_help_text = 'Поиск по модели, бренду, году выпуска, запасу хода автомобиля'
#     date_hierarchy = 'created'
#     list_per_page = 20
#
#     def preview_avatar(self, obj):
#         if obj.photo:
#             return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
#         else:
#             return 'Нет фотографии'
#
#     preview_avatar.short_description = 'Фото'
