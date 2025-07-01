from django.contrib import admin
from django.utils.safestring import mark_safe

from taxi_car.models import Address, Feedback, About, Personnel, CarBrand, Car, Reviews, Conditions, Servicing, Spares, ShopCar


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Адрес"""
    fields = 'address', 'time_work', 'phone_mtc', 'phone_a1', 'phone_life', 'maps', 'telegram', 'viber', 'whatsapp', 'instagram', 'created_year_work', 'count_car', 'rating_start', 'rating_end', 'preview_avatar', 'photo', 'created', 'updated'
    list_display = 'address', 'preview_avatar', 'time_work', 'phone_mtc', 'phone_a1', 'phone_life', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'

    def has_add_permission(self, request):
        """Создание только одной записи"""
        if Address.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Запретить удаление"""
        return False

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'


@admin.register(Servicing)
class ServicingAdmin(admin.ModelAdmin):
    """Описание работы"""
    fields = 'name', 'description', 'status', 'created', 'updated'
    list_display = 'name', 'description', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status',
    date_hierarchy = 'created'
    list_per_page = 20


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    """Условия"""
    fields = 'preview_avatar', 'photo', 'info', 'status', 'created', 'updated'
    list_display = 'info', 'preview_avatar', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status',
    date_hierarchy = 'created'
    list_per_page = 20

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'


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
    list_display = 'name', 'numbers', 'description', 'created', 'updated'
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
    """Модель автомобиля"""
    model = Car
    fields = 'photo', 'preview_avatar', 'car_brand', 'name', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
        formset.form.base_fields['year'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['power_reserve'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
        return formset

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


class SparesInline(admin.TabularInline):
    """Запчасти"""
    model = Spares
    fields = 'photo', 'preview_avatar', 'car_brand', 'name', 'price', 'description', 'availability', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """Стиль отображения"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
        formset.form.base_fields['price'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
        return formset

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


class ShopCarInline(admin.TabularInline):
    """Авто из китая"""
    model = ShopCar
    fields = 'photo', 'preview_avatar', 'car_brand', 'name', 'price', 'description', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        """Стиль отображения"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
        formset.form.base_fields['price'].widget.attrs['style'] = 'width: 60px;'
        formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
        return formset

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    """Бренд автомобиля"""
    list_display = 'name', 'car_count', 'spares_count', 'spares_availability_count', 'created', 'updated'
    date_hierarchy = 'created'
    inlines = CarInline, SparesInline, ShopCarInline
    list_per_page = 20

    def car_count(self, obj):
        """Количество моделей этого бренда"""
        return obj.car.count()

    car_count.short_description = 'Количество моделей'

    def spares_count(self, obj):
        """Количество запчастей этого бренда"""
        return obj.spares.count()

    spares_count.short_description = 'Количество запчастей'

    def spares_availability_count(self, obj):
        """Количество запчастей этого бренда"""
        return obj.spares.filter(availability=True).count()

    spares_availability_count.short_description = 'Количество запчастей в наличии'


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
