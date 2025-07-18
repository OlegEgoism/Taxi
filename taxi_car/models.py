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
    """Основные данные"""
    photo = models.ImageField(verbose_name='О нас (Фото)', upload_to='about/')
    slogan = models.TextField(verbose_name='О нас (Описание)')
    why_us_description = models.TextField(verbose_name='Почему мы (Описание)')
    name = models.CharField(verbose_name='Название организации')
    address = models.CharField(verbose_name='Адрес', max_length=100)
    time_work = models.CharField(verbose_name='Время работы', max_length=100, blank=True, null=True)
    phone_mtc = models.CharField(verbose_name='Телефон MTC', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    phone_a1 = models.CharField(verbose_name='Телефон A1', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    phone_life = models.CharField(verbose_name='Телефона Life', max_length=25, help_text='Номер телефона указывать в формате +___(__)___-__-__', blank=True, null=True)
    maps = models.TextField('Расположение на карте', help_text='Вставить скрипт-ссылку с конструктора карт https://yandex.ru/map-constructor (width="640" height="400")', blank=True, null=True)

    telegram = models.URLField(verbose_name='Telegram', blank=True, null=True, help_text='Вставить: "https://web.telegram.org/k/#" потом только свой логин @....')
    viber = models.CharField(verbose_name='Viber', blank=True, null=True, help_text='Вставить: "viber://chat?number=+" потом номер телефона 375...')
    whatsapp = models.URLField(verbose_name='Whatsapp', blank=True, null=True, help_text='Вставить: "https://wa.me/" потом номер телефона 375...')
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True)

    created_year_work = models.DateField(verbose_name='Дата начала работы компании')
    count_car = models.IntegerField(verbose_name='Автомобилей в таксопарке')
    rating_start = models.DecimalField(verbose_name='Средний рейтинг начальный', decimal_places=2, max_digits=3, validators=[MinValueValidator(1), MaxValueValidator(4.7)], help_text='Минимальное начальное значение с 1 до 4,7', default=4.7)
    rating_end = models.DecimalField(verbose_name='Средний рейтинг конечный', decimal_places=2, max_digits=3, validators=[MinValueValidator(4), MaxValueValidator(5)], help_text='Минимальное конечное значение с 4 до 5', default=5)
    telegram_bot_token = models.CharField(verbose_name='Токен бота телеграм', max_length=100, help_text='Данные из @BotFather', blank=True, null=True)
    telegram_chat_id = models.CharField(verbose_name='ID чата телеграм', max_length=100, help_text='Данные из @userinfobot', blank=True, null=True)

    def __str__(self):
        return f"{self.address} {self.time_work}"

    class Meta:
        verbose_name = 'Основные данные'
        verbose_name_plural = 'Основные данные'


class Servicing(DateStamp):
    """Почему мы"""
    photo = models.ImageField(verbose_name='О нас (Фото)', upload_to='why_us/')
    name = models.CharField(verbose_name='Название', max_length=50, help_text='Максимально 50 символов')
    description = models.TextField(verbose_name='Описание')
    numbers = models.IntegerField(verbose_name='Порядковый номер', validators=[MinValueValidator(1), MaxValueValidator(100)], unique=True)
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Сохранение фотографии формата 16:9"""
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            width, height = img.size
            target_ratio = 2 / 2
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
        verbose_name = 'Почему мы'
        verbose_name_plural = 'Почему мы'


class QuestionsAnswers(DateStamp):
    """Вопросы ответы"""
    questions = models.TextField(verbose_name='Вопрос')
    answers = models.TextField(verbose_name='Ответ')
    numbers = models.IntegerField(verbose_name='Порядковый номер', validators=[MinValueValidator(1), MaxValueValidator(100)], unique=True)
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f'{self.numbers} - {self.questions}'

    class Meta:
        verbose_name = 'Вопросы ответы'
        verbose_name_plural = 'Вопросы ответы'


class Conditions(DateStamp):
    """Банер"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='сonditions/', help_text='Фото формата 4:3')
    info = models.CharField(verbose_name='Название', max_length=60, help_text='Максимально 60 символов')
    description = models.TextField(verbose_name='Описание')
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
        verbose_name = 'Банер'
        verbose_name_plural = 'Банеры'


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
    name = models.CharField(verbose_name='Название', max_length=100, help_text='Максимально 100 символов')
    description = models.TextField(verbose_name='Описание')
    numbers = models.IntegerField(verbose_name='Порядковый номер', validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.numbers} - {self.description}"

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class CarBrand(DateStamp):
    """Автомобиль и запчасть"""
    name = models.CharField(verbose_name='Бренд', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '- Автомобили и запчасти'
        verbose_name_plural = '- Автомобили и запчасти'


class PhotoCar(models.Model):
    """Фото таксопарка"""
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='cars', verbose_name='Автомобиль')
    photo = models.ImageField(verbose_name='Фото', upload_to='car/')

    def __str__(self):
        return f'Фото {self.car}'

    class Meta:
        verbose_name = 'Фото таксопарка'
        verbose_name_plural = 'Фото таксопарка'


class Car(DateStamp):
    """Таксопарк"""
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE, related_name='car')
    name = models.CharField(verbose_name='Модель', max_length=100)
    year = models.IntegerField(verbose_name='Год выпуска', validators=[MinValueValidator(2000), MaxValueValidator(2050)])
    power_reserve = models.IntegerField(verbose_name='Запас хода км.', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f'{self.car_brand} {self.name}'

    class Meta:
        verbose_name = 'Таксопарк'
        verbose_name_plural = '2. Таксопарк'


class PhotoSpares(models.Model):
    """Фото запчастей"""
    spare = models.ForeignKey('Spares', on_delete=models.CASCADE, related_name='spares', verbose_name='Запчасти')
    photo = models.ImageField(verbose_name='Фото', upload_to='spare/')

    def __str__(self):
        return f'Фото {self.spare}'

    class Meta:
        verbose_name = 'Фото запчастей'
        verbose_name_plural = 'Фото запчастей'


class Spares(DateStamp):
    """Запчасти"""
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE, related_name='spare')
    name = models.CharField(verbose_name='Название запчасти', max_length=100)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, validators=[MinValueValidator(1), MaxValueValidator(50000)], blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    availability = models.BooleanField(verbose_name='Наличие', default=True)
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f'{self.car_brand} {self.name}'

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = '3. Запчасти'


class PhotoShopCar(models.Model):
    """Фото авто из китая"""
    shop = models.ForeignKey('ShopCar', on_delete=models.CASCADE, related_name='shops', verbose_name='Авто из китая')
    photo = models.ImageField(verbose_name='Фото', upload_to='shop/')

    def __str__(self):
        return f'Фото {self.shop}'

    class Meta:
        verbose_name = 'Фото авто из китая'
        verbose_name_plural = 'Фото авто из китая'


class ShopCar(DateStamp):
    """Авто из китая"""
    car_brand = models.ForeignKey(to=CarBrand, verbose_name='Бренд автомобиля', on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(verbose_name='Название модели', max_length=100)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, validators=[MinValueValidator(1), MaxValueValidator(50000)], blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return f'{self.car_brand} {self.name}'

    class Meta:
        verbose_name = 'Авто из китая'
        verbose_name_plural = '1. Авто из китая'


class Reviews(DateStamp):
    """Отзывы"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='reviews/', help_text='Фото формата 4:3')
    name = models.CharField(verbose_name='Имя', max_length=30)
    message = models.TextField(verbose_name='Текст сообщения')
    status = models.BooleanField(verbose_name='Опубликован', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
