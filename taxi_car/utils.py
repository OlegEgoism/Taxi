import os
import requests
import random
import time
from datetime import date
from datetime import datetime


def message_to_telegram(name, phone_email, message, bot_token, chat_id):
    """Отправить сообщение в телеграмм"""
    text = (f"💬 *Новое сообщение* ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n\n"
            f"👤 *Имя:* {name}\n"
            f"📞 *Контакт:* {phone_email}\n"
            f"✉️ *Сообщение:* {message}")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    return response.ok


RATING_CACHE = {
    'value': 4.5,
    'timestamp': 0,
    'start': None,
    'end': None,
}


def get_random_rating(address):
    """Рейтинг"""
    now = time.time()
    if not address:
        rating_start = 4.2
        rating_end = 4.8
    else:
        rating_start = float(address.rating_start or 4.2)
        rating_end = float(address.rating_end or 4.8)
    if (now - RATING_CACHE['timestamp'] > 30 * 60 or
            RATING_CACHE['start'] != rating_start or
            RATING_CACHE['end'] != rating_end):
        RATING_CACHE['start'] = rating_start
        RATING_CACHE['end'] = rating_end
        RATING_CACHE['value'] = round(random.uniform(rating_start, rating_end), 2)
        RATING_CACHE['timestamp'] = now
    return RATING_CACHE['value']


def calculate_passengers(address):
    """Расчет перевезенных пассажиров"""
    if not address or not address.created_year_work or not address.count_car:
        return 0
    days = (date.today() - address.created_year_work).days
    print(days)
    count_car = address.count_car
    multiplier = 7
    return days * count_car * multiplier


def get_years_work(address):
    """Расчет количество опыта работы"""
    if not address or not address.created_year_work:
        return 0
    today = date.today()
    years = today.year - address.created_year_work.year
    if (today.month, today.day) < (address.created_year_work.month, address.created_year_work.day):
        years -= 1
    return years


def years_word(n):
    """Склонения для русского языка"""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return "год"
    elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "года"
    else:
        return "лет"
