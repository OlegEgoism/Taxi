from django.contrib import admin
from django.utils.safestring import mark_safe

from taxi_car.models import Address, Feedback, About, CarBrand, Car, Reviews, Conditions, Servicing, Spares, ShopCar, QuestionsAnswers, PhotoCar, PhotoSpares, PhotoShopCar


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Основные данные"""
    fields = ('preview_avatar', 'photo', 'slogan', 'why_us_description', 'name', 'address', 'time_work', 'phone_mtc',
              'phone_a1', 'phone_life', 'maps', 'telegram', 'viber', 'whatsapp', 'instagram', 'created_year_work',
              'count_car', 'rating_start', 'rating_end', 'telegram_bot_token', 'telegram_chat_id', 'created', 'updated')
    list_display = 'name', 'address', 'time_work', 'phone_mtc', 'phone_a1', 'phone_life', 'created', 'updated'
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

    preview_avatar.short_description = 'О нас (Фото)'


@admin.register(Servicing)
class ServicingAdmin(admin.ModelAdmin):
    """Почему мы"""
    fields = 'preview_avatar', 'photo', 'name', 'description', 'numbers', 'status', 'created', 'updated'
    list_display = 'preview_avatar', 'name', 'description', 'numbers', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status',
    date_hierarchy = 'created'
    ordering = 'numbers',
    list_per_page = 20

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'


@admin.register(QuestionsAnswers)
class QuestionsAnswersAdmin(admin.ModelAdmin):
    """Вопросы ответы"""
    fields = 'questions', 'answers', 'numbers', 'status', 'created', 'updated'
    list_display = 'questions', 'answers', 'numbers', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status',
    date_hierarchy = 'created'
    ordering = 'numbers',
    list_per_page = 20


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    """Банер"""
    fields = 'preview_avatar', 'photo', 'info', 'description', 'status', 'created', 'updated'
    list_display = 'preview_avatar', 'info', 'description', 'status', 'created', 'updated'
    readonly_fields = 'preview_avatar', 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status',
    date_hierarchy = 'created'
    list_per_page = 20

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'info' in form.base_fields:
            form.base_fields['info'].widget.attrs['style'] = 'width: 40%;'
        return form

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60"/>')
        else:
            return 'Нет фотографии'

    preview_avatar.short_description = 'Фото'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Обратная связь"""
    list_display = 'name', 'phone_email', 'message', 'published', 'created',
    list_filter = 'published', 'created', 'updated'
    list_editable = 'published',
    readonly_fields = 'name', 'phone_email', 'message', 'published', 'created',
    search_fields = 'name', 'phone_email', 'email'
    search_help_text = 'Поиск по имени, телефону или почте'
    date_hierarchy = 'created'
    list_per_page = 20

    def has_add_permission(self, request):
        """Запрещает добавление"""
        return False

    def has_delete_permission(self, request, obj=None):
        """По желанию: запретить и удаление"""
        return False


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """О нас"""
    fields = 'name', 'description', 'numbers', 'created', 'updated'
    list_display = 'name', 'description', 'numbers', 'created', 'updated'
    readonly_fields = 'created', 'updated',
    date_hierarchy = 'created'
    ordering = 'numbers',
    list_per_page = 20


class PhotoCarInline(admin.TabularInline):
    """Фото таксопарка"""
    model = PhotoCar
    fields = 'photo', 'preview_avatar', 'car',
    readonly_fields = 'preview_avatar',
    extra = 1

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Таксопарк"""
    list_display = 'car_brand', 'name', 'year', 'power_reserve', 'short_description', 'photo_count', 'status', 'created', 'updated'
    fields = 'car_brand', 'name', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status', 'car_brand__name', 'created', 'updated'
    inlines = [PhotoCarInline]

    def photo_count(self, obj):
        """Количество фото"""
        return obj.cars.count()

    photo_count.short_description = 'Количество фото'

    def short_description(self, obj):
        """Краткое описание"""
        text = obj.description or ""
        return (text[:50] + '...') if len(text) > 20 else text

    short_description.short_description = 'Описание'


class PhotoSparesInline(admin.TabularInline):
    """Фото запчастей"""
    model = PhotoSpares
    fields = 'photo', 'preview_avatar', 'spare',
    readonly_fields = 'preview_avatar',
    extra = 1

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


@admin.register(Spares)
class SparesAdmin(admin.ModelAdmin):
    """Запчасти"""
    list_display = 'car_brand', 'name', 'price', 'short_description', 'photo_count', 'availability', 'status', 'created', 'updated'
    fields = 'car_brand', 'name', 'price', 'description', 'availability', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    list_editable = 'availability', 'status',
    list_filter = 'availability', 'status', 'car_brand__name', 'created', 'updated'
    inlines = [PhotoSparesInline]

    def photo_count(self, obj):
        """Количество фото"""
        return obj.spares.count()

    photo_count.short_description = 'Количество фото'

    def short_description(self, obj):
        """Краткое описание"""
        text = obj.description or ""
        return (text[:50] + '...') if len(text) > 20 else text

    short_description.short_description = 'Описание'


class PhotoShopCarInline(admin.TabularInline):
    """Фото авто из китая"""
    model = PhotoShopCar
    fields = 'photo', 'preview_avatar', 'shop',
    readonly_fields = 'preview_avatar',
    extra = 1

    def preview_avatar(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return 'Нет фото'

    preview_avatar.short_description = 'Фото'


@admin.register(ShopCar)
class ShopCarAdmin(admin.ModelAdmin):
    """Авто из китая"""
    list_display = 'car_brand', 'name', 'price', 'short_description', 'photo_count', 'status', 'created', 'updated'
    fields = 'car_brand', 'name', 'price', 'description', 'status', 'created', 'updated'
    readonly_fields = 'created', 'updated'
    list_editable = 'status',
    list_filter = 'status', 'car_brand__name', 'created', 'updated'
    inlines = [PhotoShopCarInline]

    def photo_count(self, obj):
        """Количество фото"""
        return obj.shops.count()

    photo_count.short_description = 'Количество фото'

    def short_description(self, obj):
        """Краткое описание"""
        text = obj.description or ""
        return (text[:50] + '...') if len(text) > 20 else text

    short_description.short_description = 'Описание'


class CarInline(admin.TabularInline):
    """Модель автомобиля (только просмотр)"""
    model = Car
    fields = 'car_brand', 'name', 'year', 'power_reserve', 'description', 'status', 'created', 'updated'
    readonly_fields = 'car_brand', 'name', 'year', 'power_reserve', 'description', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
    #     formset.form.base_fields['year'].widget.attrs['style'] = 'width: 60px;'
    #     formset.form.base_fields['power_reserve'].widget.attrs['style'] = 'width: 60px;'
    #     formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
    #     return formset


class SparesInline(admin.TabularInline):
    """Запчасти"""
    model = Spares
    fields = 'car_brand', 'name', 'price', 'description', 'availability', 'status', 'created', 'updated'
    readonly_fields = 'car_brand', 'name', 'price', 'description', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def get_formset(self, request, obj=None, **kwargs):
    #     """Стиль отображения"""
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
    #     formset.form.base_fields['price'].widget.attrs['style'] = 'width: 60px;'
    #     formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
    #     return formset


class ShopCarInline(admin.TabularInline):
    """Авто из китая"""
    model = ShopCar
    fields = 'car_brand', 'name', 'price', 'description', 'status', 'created', 'updated'
    readonly_fields = 'car_brand', 'name', 'price', 'description', 'created', 'updated'
    classes = ['collapse']
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def get_formset(self, request, obj=None, **kwargs):
    #     """Стиль отображения"""
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['name'].widget.attrs['style'] = 'width: 180px;'
    #     formset.form.base_fields['price'].widget.attrs['style'] = 'width: 60px;'
    #     formset.form.base_fields['description'].widget.attrs['style'] = 'width: 360px;'
    #     return formset


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    """Бренд автомобиля"""
    pass
    list_display = 'name', 'car_count', 'shop_car_count', 'spares_count', 'spares_availability_count', 'created', 'updated'
    date_hierarchy = 'created'
    inlines = ShopCarInline, CarInline, SparesInline,
    list_per_page = 20

    def car_count(self, obj):
        """Количество моделей этого бренда"""
        return obj.car.count()

    car_count.short_description = 'Количество таксопарка'

    def shop_car_count(self, obj):
        """Количество авто из китая"""
        return obj.shop.count()

    shop_car_count.short_description = 'Количество авто из китая'

    def spares_count(self, obj):
        """Количество запчастей этого бренда"""
        return obj.spare.count()

    spares_count.short_description = 'Количество запчастей'

    def spares_availability_count(self, obj):
        """Количество запчастей этого бренда"""
        return obj.spare.filter(availability=True).count()

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
