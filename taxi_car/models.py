from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PIL import Image


class DateStamp(models.Model):
    """Временные отметки"""
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Address(DateStamp):
    """Адрес"""
    address = models.CharField(verbose_name='Адрес', max_length=100)
    time_work = models.CharField(verbose_name='Время работы', max_length=100)
    phone_mtc = models.CharField(verbose_name='Телефон MTC', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    phone_a1 = models.CharField(verbose_name='Телефон A1', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    phone_life = models.CharField(verbose_name='Телефона Life', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    maps = models.TextField('Расположение на карте', help_text='Вставить скрипт-ссылку с конструктора карт https://yandex.ru/map-constructor (width="640" height="400")', blank=True, null=True)
    telegram = models.URLField(verbose_name='Telegram', blank=True, null=True)
    viber = models.URLField(verbose_name='Viber', blank=True, null=True)
    whatsapp = models.URLField(verbose_name='Whatsapp', blank=True, null=True)
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True)
    year_work = models.IntegerField(verbose_name='Лет опыта')
    count_car = models.IntegerField(verbose_name='Автомобилей в таксопарке')
    transported = models.IntegerField(verbose_name='Перевезенных пассажиров')
    rating = models.DecimalField(verbose_name='Средний рейтинг', decimal_places=2, max_digits=3, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.address} {self.time_work}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адрес'


class Feedback(DateStamp):
    """Обратная связь"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    phone_email = models.CharField(verbose_name='Телефон или почта', max_length=50, blank=True, null=True)
    message = models.TextField(verbose_name='Сообщение')
    published = models.BooleanField(verbose_name='Обработано', default=False)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.phone_email or ''


class About(DateStamp):
    """О нас"""
    numbers = models.IntegerField(verbose_name='Порядковый номер', validators=[MinValueValidator(1), MaxValueValidator(10)])
    name = models.CharField(verbose_name='Название', max_length=50)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f"{self.numbers} - {self.description}"

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class Personnel(DateStamp):
    """Сотрудник"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='photo/', help_text='Фото формата 4:3')
    fio = models.CharField(verbose_name='ФИО', max_length=50)
    position = models.CharField(verbose_name='Должность', max_length=50)
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f"{self.fio} - {self.position}"

    def save(self, *args, **kwargs):
        """Сохранение фотографии формата 16:9"""
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            width, height = img.size
            target_ratio = 4 / 3
            current_ratio = width / height
            if current_ratio > target_ratio:
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img_cropped = img.crop((left, 0, left + new_width, height))
            else:
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img_cropped = img.crop((0, top, width, top + new_height))
            img_cropped.save(self.photo.path)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class CarBrand(DateStamp):
    """Бренд автомобиля"""
    name = models.CharField(verbose_name='Бренд', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Car(DateStamp):
    """Модель автомобиля"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='car/', help_text='Фото формата 16:9')
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Модель', max_length=100)
    year = models.IntegerField(verbose_name='Год выпуска', validators=[MinValueValidator(2000), MaxValueValidator(2050)])
    power_reserve = models.CharField(verbose_name='Запас хода', max_length=10, blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f'{self.car_brand} {self.name}'

    def save(self, *args, **kwargs):
        """Сохранение фотографии формата 16:9"""
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            width, height = img.size
            target_ratio = 16 / 9
            current_ratio = width / height
            if current_ratio > target_ratio:
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img_cropped = img.crop((left, 0, left + new_width, height))
            else:
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img_cropped = img.crop((0, top, width, top + new_height))
            img_cropped.save(self.photo.path)

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'



class Reviews(DateStamp):
    """Отзывы"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='reviews/', help_text='Фото формата 4:3')
    name = models.CharField(verbose_name='Имя', max_length=30)
    message = models.TextField(verbose_name='Текст сообщения')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Сохранение фотографии формата 4:3"""
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            width, height = img.size
            target_ratio = 4 / 3
            current_ratio = width / height
            if current_ratio > target_ratio:
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img_cropped = img.crop((left, 0, left + new_width, height))
            else:
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img_cropped = img.crop((0, top, width, top + new_height))
            img_cropped.save(self.photo.path)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'