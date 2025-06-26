from django.shortcuts import render
from taxi_car.models import Address


def home(request):
    """Главная страница"""
    address = Address.objects.first()
    return render(request, template_name='index.html', context={'address': address})


def contact(request):
    """Контакты"""
    address = Address.objects.first()
    return render(request, template_name='contact.html', context={'address': address})


def about(request):
    """О нас"""
    return render(request, 'about.html')


def car(request):
    """Таксопарк"""
    return render(request, 'car.html')


def service(request):
    """Запчасти"""
    return render(request, 'service.html')
