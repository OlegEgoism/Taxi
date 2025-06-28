import os
import requests
from datetime import datetime
from taxi_car.models import Address, About, Personnel, Car, Reviews
from .forms import FeedbackForm
from django.shortcuts import render, redirect
from django.contrib import messages
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')


def message_to_telegram(name, phone_email, message, bot_token, chat_id):
    """Отправить сообщение в телеграмм"""
    text = (f"💬 *Новое сообщение* ({datetime.now().strftime("%d-%m-%Y %H:%M:%S")})\n\n"
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


def home(request):
    """Главная страница"""
    address = Address.objects.first()
    reviews = Reviews.objects.filter(status=True)
    return render(request,
                  template_name='index.html',
                  context={'address': address,
                           'reviews': reviews})


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
    cars = Car.objects.filter(status=True)
    return render(request,
                  template_name='car.html',
                  context={'address': address,
                           'cars': cars})


def service(request):
    """Запчасти"""
    return render(request, 'service.html')




    # def send_telegram_notification(name, contact, message):
    #     """Отправка уведомления в Telegram"""
    #     bot_token = TELEGRAM_BOT_TOKEN
    #     chat_id = TELEGRAM_CHAT_ID
    #
    #     if not bot_token or not chat_id:
    #         print("Telegram settings not configured!")
    #         return
    #
    #     text = (f"📨 Новое сообщение из формы обратной связи\n\n"
    #             f"👤 Имя: {name}\n"
    #             f"📞 Контакты: {contact}\n"
    #             f"📝 Сообщение: {message}")
    #
    #     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    #     params = {
    #         'chat_id': chat_id,
    #         'text': text
    #     }
    #     try:
    #         response = requests.post(url, params=params)
    #         response.raise_for_status()
    #     except Exception as e:
    #         print(f"Ошибка при отправке в Telegram: {e}")
    #
    #
    # def contact(request):
    #     """Контакты"""
    #     address = Address.objects.first()
    #     if request.method == 'POST':
    #         name = request.POST.get('name')
    #         phone_email = request.POST.get('phone_email')
    #         message = request.POST.get('message')
    #
    #         # Сохраняем в базу данных
    #         feedback = Feedback.objects.create(
    #             name=name,
    #             phone_email=phone_email,
    #             message=message,
    #             published=False
    #         )
    #         print(feedback)
    #
    #         send_telegram_notification(name, phone_email, message)
    #         messages.success(request, 'Ваше сообщение успешно отправлено!')
    #         return redirect('contact')
    #
    #     return render(request, template_name='contact.html', context={'address': address})
    #

    # def contact(request):
    #     if request.method == 'POST':
    #         phone_form = FeedbackForm(request.POST)
    #         if phone_form.is_valid():
    #             updated_values = {'complete': False}
    #             phone_email = phone_form.cleaned_data['phone_email']
    #             Feedback.objects.update_or_create(user_tel=phone_email, defaults=updated_values)
    #             response = requests.post(
    #                 url=f'https://api.telegram.org/bot{tele_bot_token}/sendMessage',
    #                 data={'chat_id': chat_id,
    #                       'text': f'*Поступила новая заявка:*\n\n{phone_email}',
    #                       'parse_mode': 'markdown'}
    #             ).json()
    #             if not response.get('ok', False):
    #                 warnings.warn(f'''
    #                 ВНИМАНИЕ!!!
    #                 Не удалось отправить сообщение телеграм боту или формат ответа изменился.
    #                 Код ошибки: {response.get("error_code", "Не удалось получить код ошибки.")}
    #                 Описание ошибки: {response.get("description", "Не удалось получить описание ошибки.")}''')
    #             return redirect('contact')
    #     address = Address.objects.first()
    #     context = {'address': address}
    #     return render(request, 'contact.html', context)

    # def contact(request):
    #     address = Address.objects.first()  # Получаем адрес заранее
    #     if request.method == 'POST':
    #         form = FeedbackForm(request.POST)
    #         if form.is_valid():
    #             feedback = form.save()
    #             # Отправка в Telegram
    #             phone_email = feedback.phone_email or ''
    #             name = feedback.name or ''
    #             message_text = feedback.message or ''
    #             text = (
    #                 f"*Поступила новая заявка:*\n\n"
    #                 f"*Имя:* {name}\n"
    #                 f"*Контакт:* {phone_email}\n"
    #                 f"*Сообщение:* {message_text}"
    #             )
    #             response = requests.post(
    #                 url=f'https://api.telegram.org/bot{tele_bot_token}/sendMessage',
    #                 data={
    #                     'chat_id': chat_id,
    #                     'text': text,
    #                     'parse_mode': 'Markdown'
    #                 }
    #             ).json()
    #             if not response.get('ok', False):
    #                 warnings.warn(
    #                     f"ВНИМАНИЕ!!!\n"
    #                     f"Не удалось отправить сообщение телеграм боту или формат ответа изменился.\n"
    #                     f"Код ошибки: {response.get('error_code', 'Не удалось получить код ошибки.')}\n"
    #                     f"Описание ошибки: {response.get('description', 'Не удалось получить описание ошибки.')}"
    #                 )
    #             messages.success(request, 'Сообщение отправлено! Спасибо за обратную связь.')
    #             return redirect('contact')
    #     else:
    #         form = FeedbackForm()
    #     context = {'form': form, 'address': address}
    #     return render(request, 'contact.html', context)
