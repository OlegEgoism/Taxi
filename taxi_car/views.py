from taxi_car.models import Address, About, Personnel, Car, Reviews, Conditions, Servicing, Spares, CarBrand, ShopCar
from .forms import FeedbackForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .utils import message_to_telegram, bot_token, chat_id, get_random_rating, calculate_passengers, get_years_work, years_word


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
    conditions = Conditions.objects.filter(status=True)
    reviews = Reviews.objects.filter(status=True)
    servicing = Servicing.objects.filter(status=True)
    random_rating = get_random_rating(address)
    passenger_count = calculate_passengers(address)
    years_work = get_years_work(address)
    years_word_str = years_word(years_work)
    return render(request,
                  template_name='index.html',
                  context={
                      'address': address,
                      'servicing': servicing,
                      'conditions': conditions,
                      'reviews': reviews,
                      'random_rating': random_rating,
                      'passenger_count': passenger_count,
                      'years_work': years_work,
                      'years_word': years_word_str,
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
    brand_id = request.GET.get('brand', '')
    brands = CarBrand.objects.all()
    spares = Spares.objects.filter(status=True)
    if brand_id:
        spares = Spares.objects.filter(status=True, car_brand_id=brand_id)
        if query:
            spares = spares.filter(
                Q(name__iregex=query) |
                Q(car_brand__name__iregex=query) |
                Q(description__iregex=query)
            )
    return render(request,
                  template_name='service.html',
                  context={'address': address,
                           'spares': spares,
                           'brands': brands,
                           'active_brand': int(brand_id) if brand_id.isdigit() else None,
                           'query': query,
                           })


def shop_car(request):
    """Авто из Китая"""
    address = Address.objects.first()
    brands = CarBrand.objects.all()
    shop_cars = ShopCar.objects.filter(status=True)
    return render(request,
                  template_name='shop_car.html',
                  context={'address': address,
                           'brands': brands,
                           'shop_cars': shop_cars,
                           })


def custom_404(request, exception):
    """Страница не найдена"""
    address = Address.objects.first()
    return render(request,
                  template_name='404.html',
                  context={'address': address},
                  status=404)
