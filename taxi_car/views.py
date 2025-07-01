import os
import requests
import random
import time
from datetime import datetime
from taxi_car.models import Address, About, Personnel, Car, Reviews, Conditions, Servicing, Spares
from .forms import FeedbackForm
from django.shortcuts import render, redirect
from django.contrib import messages
from dotenv import load_dotenv
from django.db.models import Q


load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')


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


def contact(request):
    """Контакты"""
    address = Address.objects.first()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            message_to_telegram(
                feedback.name,
                feedback.phone_email,
                feedback.message,
                bot_token,
                chat_id
            )
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('contact')
    else:
        form = FeedbackForm()
    return render(request,
                  template_name='contact.html',
                  context={'address': address,
                           'form': form})


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
        rating_start = 4
        rating_end = 4.5
    else:
        rating_start = float(address.rating_start or 4)
        rating_end = float(address.rating_end or 4.5)
    if (now - RATING_CACHE['timestamp'] > 0.1 * 60 or
            RATING_CACHE['start'] != rating_start or
            RATING_CACHE['end'] != rating_end):
        RATING_CACHE['start'] = rating_start
        RATING_CACHE['end'] = rating_end
        RATING_CACHE['value'] = round(random.uniform(rating_start, rating_end), 2)
        RATING_CACHE['timestamp'] = now
    return RATING_CACHE['value']


def home(request):
    """Главная страница"""
    address = Address.objects.first()
    conditions = Conditions.objects.filter(status=True)
    reviews = Reviews.objects.filter(status=True)
    servicing = Servicing.objects.filter(status=True)
    random_rating = get_random_rating(address)
    return render(request,
                  template_name='index.html',
                  context={
                      'address': address,
                      'servicing': servicing,
                      'conditions': conditions,
                      'reviews': reviews,
                      'random_rating': random_rating
                  })


def about(request):
    """О нас"""
    address = Address.objects.first()
    about_info = About.objects.all()
    personnel = Personnel.objects.filter(status=True)
    return render(request,
                  template_name='about.html',
                  context={'address': address,
                           'about_info': about_info,
                           'personnel': personnel})


def car(request):
    """Таксопарк"""
    address = Address.objects.first()
    cars = Car.objects.filter(status=True).order_by('car_brand__name', 'name')
    return render(request,
                  template_name='car.html',
                  context={'address': address,
                           'cars': cars})




def service(request):
    """Запчасти"""
    address = Address.objects.first()
    query = request.GET.get('q', '').strip()
    spares = Spares.objects.filter(status=True)
    if query:
        spares = spares.filter(
            Q(car_brand__name__icontains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request,
                  template_name='service.html',
                  context={'address': address,
                           'spares': spares,
                           'query': query})


def custom_404(request, exception):
    """Страница не найдена"""
    address = Address.objects.first()
    return render(request,
                  template_name='404.html',
                  context={'address': address},
                  status=404)
