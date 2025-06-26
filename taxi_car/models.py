from django.db import models


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
    maps = models.TextField('Расположение на карте', help_text='Вставить скрипт-ссылку с конструктора карт https://yandex.ru/map-constructor (width="640" height="500")', blank=True, null=True)
    telegram = models.URLField(verbose_name='Telegram', blank=True, null=True)
    viber = models.URLField(verbose_name='Viber', blank=True, null=True)
    whatsapp = models.URLField(verbose_name='Whatsapp', blank=True, null=True)
    instagram = models.URLField(verbose_name='Instagram', blank=True, null=True)

    def __str__(self):
        return f"{self.address} {self.time_work}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адрес'


class Feedback(DateStamp):
    """Обратная связь"""
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('Почта', max_length=50, blank=True, null=True)
    message = models.TextField('Сообщение')
    published = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'{self.phone} {self.email}'
