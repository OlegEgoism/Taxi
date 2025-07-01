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
    created_year_work = models.DateField(verbose_name='Дата начала работы компании')
    count_car = models.IntegerField(verbose_name='Автомобилей в таксопарке')
    rating_start = models.DecimalField(verbose_name='Средний рейтинг начальный', decimal_places=2, max_digits=3, validators=[MinValueValidator(1), MaxValueValidator(4)], help_text='Минимальное начальное значение с 1 до 4', default=4)
    rating_end = models.DecimalField(verbose_name='Средний рейтинг конечный', decimal_places=2, max_digits=3, validators=[MinValueValidator(4), MaxValueValidator(5)], help_text='Минимальное конечное значение с 4 до 5', default=4.5)
    photo = models.ImageField(verbose_name='Изображение на странице о нас', upload_to='about/')

    def __str__(self):
        return f"{self.address} {self.time_work}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адрес'


class Servicing(DateStamp):
    """Описание работы"""
    name = models.CharField(verbose_name='Название', max_length=50)
    description = models.TextField(verbose_name='Описание')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Описание работы'
        verbose_name_plural = 'Описание работы'


class Conditions(DateStamp):
    """Условия"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='сonditions/', help_text='Фото формата 4:3')
    info = models.CharField(verbose_name='Условия', max_length=100)
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f"{self.info}"

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
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'


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
    """Сотрудники"""
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
    """Автомобиль и запчасть"""
    name = models.CharField(verbose_name='Бренд', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автомобиль и запчасть'
        verbose_name_plural = 'Автомобили и запчасти'


class Car(DateStamp):
    """Модель автомобиля"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='car/', help_text='Фото формата 16:9')
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE, related_name='car')
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


class Spares(DateStamp):
    """Запчасти"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='car/', help_text='Фото формата 16:9')
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE, related_name='spares')
    name = models.CharField(verbose_name='Название запчасти', max_length=100)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, validators=[MinValueValidator(1), MaxValueValidator(50000)], blank=True, null=True)
    guarantee = models.IntegerField(verbose_name='Гарантия (лет)', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    availability = models.BooleanField(verbose_name='Наличие', default=True)
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

    def guarantee_word(self):
        """Отображение слова"""
        n = self.guarantee or 0
        if 11 <= (n % 100) <= 14:
            return 'лет'
        last = n % 10
        if last == 1:
            return 'год'
        elif 2 <= last <= 4:
            return 'года'
        else:
            return 'лет'

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'


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
