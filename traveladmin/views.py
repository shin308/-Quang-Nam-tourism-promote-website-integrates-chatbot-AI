from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# from flask import request
from travello.chatbot_run import chatbot_response
from scrape import scrape_data

from travello.models import Detailed_desc
from travello.models import Destination
from travello.models import Places
from travello.models import Travel_types
from travello.models import Specialties
from travello.models import Specialties_types
from travello.models import pessanger_detail
from travello.models import Transactions
# Create your views here.

def admin_login(request):
    try:
        # if request.user.is_superuser:

        # if request.user.is_authenticated:
        #     return redirect('/admin-home')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username = username, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard')
            
            messages.info(request, 'Invalid password')
            return redirect('/')

        return render(request, 'login-admin.html')
    except Exception as e:
        print(e)

# @user_passes_test(lambda u: u.is_superuser)
def logout_admin(request):
    auth.logout(request)
    return redirect('/admin-home')

# @user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    users = User.objects.filter(is_superuser = 0).count()
    dest = Destination.objects.all().count()
    dest_detail = Detailed_desc.objects.all().count()
    booked = pessanger_detail.objects.filter(pay_done = 1).count()
    places = Places.objects.all().count()
    foods = Specialties.objects.all().count()

    return render(request, 'dashboard.html', {'users': users, 'dest':dest, 'dest_detail':dest_detail, 
                            'booked': booked, 'places': places, 'foods': foods})

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser)
def destination(request):
    dess = Destination.objects.all()

    context = {
        'dess': dess,
    }
    return render(request, 'destination.html', context)

@login_required(login_url='admin-login')
def add_destination(request):
    if request.method == "POST":
        id = request.POST.get('id')
        country = request.POST.get('country')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        number = Detailed_desc.objects.filter(country = country).count()

        dess = Destination(
            id = id,
            country = country,
            img1 = img1,
            img2= img2,
            number = number
        )
        dess.save()
        return redirect('destination')

    return render(request, 'destination.html')

@login_required(login_url='admin-login')
def edit_destination(request):
    dess = Destination.objects.all()

    context = {
        'dess': dess,
    }
    return redirect(request, 'destination.html', context)

@login_required(login_url='admin-login')
def update_destination(request, id):
    if request.method == "POST":
        country = request.POST.get('country')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        number = request.POST.get('number')
        number = Detailed_desc.objects.filter(country = country).count()

        dess = Destination(
            id = id,
            country = country,
            img1 = img1,
            img2 = img2,
            number = number
        )
        dess.save()
        return redirect('/admin-home/destination')

    return redirect(request, 'destination.html')

@login_required(login_url='admin-login')
def delete_destination(request, id):
    dess = Destination.objects.filter(id = id).delete()
    
    # context = {
    #     dess: 'dess'
    # }

    return redirect('/admin-home/destination')

def destination_details(request):
    dess = Detailed_desc.objects.all()
    dest = Destination.objects.all()

    context = {
        'dess': dess,
        'dest': dest
    }
    return render(request, 'destination-desc.html', context)

def add_destination_details(request):
    if request.method == "POST":
        id = request.POST.get("id")
        country = request.POST.get("country")
        days = request.POST.get("days")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        name = request.POST.get("name")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        description = request.POST.get("description")
        day1 = request.POST.get("day1")
        day2 = request.POST.get("day2")
        day3 = request.POST.get("day3")
        day4 = request.POST.get("day4")
        day5 = request.POST.get("day5")
        day6 = request.POST.get("day6")
        trip_date = request.POST.get("trip_date")
        num_booking = request.POST.get('num_booking')
        number = Detailed_desc.objects.filter(country = country).count()
        dest = Destination.objects.get(country = country)

        dess = Detailed_desc(
            dest_id = id,
            country = country,
            days = days,
            price = price,
            rating = rating,
            dest_name = name,
            img1 = img1,
            img2 = img2,
            desc = description,
            day1 = day1,
            day2 = day2,
            day3 = day3,
            day4 = day4,
            day5 = day5,
            day6 = day6,
            trip_date = trip_date,
            num_bookings = num_booking
        )
        dess.save()

        dest.number = number
        dest.save(update_fields=['number'])
        dest.save()
        
        return redirect('destination-details')

    return render(request, 'destination-desc.html')

def edit_destination_details(request):
    dess = Detailed_desc.objects.all()

    context = {
        'dess': dess,
    }
    return redirect(request, 'destination.html', context)

def update_destination_details(request, id):
    if request.method == "POST":
        country = request.POST.get("country")
        days = request.POST.get("days")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        name = request.POST.get("name")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        description = request.POST.get("description")
        day1 = request.POST.get("day1")
        day2 = request.POST.get("day2")
        day3 = request.POST.get("day3")
        day4 = request.POST.get("day4")
        day5 = request.POST.get("day5")
        day6 = request.POST.get("day6")
        trip_date = request.POST.get("trip_date")
        num_booking = request.POST.get('num_booking')
        number = Detailed_desc.objects.filter(country = country).count()
        dest = Destination.objects.get(country = country)

        dess = Detailed_desc(
            dest_id = id,
            country = country,
            days = days,
            price = price,
            rating = rating,
            dest_name = name,
            img1 = img1,
            img2 = img2,
            desc = description,
            day1 = day1,
            day2 = day2,
            day3 = day3,
            day4 = day4,
            day5 = day5,
            day6 = day6,
            trip_date = trip_date,
            num_bookings = num_booking
        )

        dess.save()

        dest.number = number
        dest.save(update_fields=['number'])
        dest.save()

        return redirect('/admin-home/destination-details')

    return render(request, 'destination-desc.html')
    
def delete_destination_details(request, id):
    dess = Detailed_desc.objects.filter(dest_id = id).delete()
    
    # context = {
    #     dess: 'dess'
    # }

    return redirect('/admin-home/destination-details')

def users(request):
    users = User.objects.filter(is_superuser = 0)

    context = {
        'users': users,
    }
    return render(request, 'users.html', context)

def edit_users(request):
    users = User.objects.filter(is_superuser = 0)

    context = {
        'users': users,
    }

    return redirect(request, 'users.html', context)

def delete_users(request, id):
    users = User.objects.filter(id = id).delete()

    return redirect('/admin-home/users')

def places_list(request):
    types = Travel_types.objects.all()
    places = Places.objects.all()

    context = {'places': places, 'types': types}
    return render(request, 'places-list.html', context)

def add_place(request):
    if request.method == "POST":
        id = request.POST.get("id")
        city = request.POST.get("city")
        type = request.POST.get("type_place")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        name = request.POST.get("name")
        address = request.POST.get("address")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        img3 = request.POST.get("img3")
        img4 = request.POST.get("img4")
        img5 = request.POST.get("img5")
        description = request.POST.get("description")
        open_time = request.POST.get("open_time")
        close_time = request.POST.get("close_time")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        map = request.POST.get("map")
        short_name = request.POST.get("short_name")

        places = Places(
            district = city,
            type_place = type,
            price = price,
            rating = rating,
            dest_name = name,
            img1 = img1,
            img2 = img2,
            img3 = img3,
            img4 = img4,
            img5 = img5,
            desc = description,
            address = address,
            open_time = open_time,
            close_time = close_time,
            email = email,
            phone = phone,
            place_map = map,
            place_name_short = short_name,
        )

        places.save()
        return redirect('places-list')

    return render(request, 'places-list.html')

def edit_place(request):
    places = Places.objects.all()

    context = {
        'places': places,
    }
    return redirect(request, 'places-list.html', context)

def update_place(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        city = request.POST.get("city")
        type = request.POST.get("type_place")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        name = request.POST.get("name")
        address = request.POST.get("address")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        img3 = request.POST.get("img3")
        img4 = request.POST.get("img4")
        img5 = request.POST.get("img5")
        description = request.POST.get("description")
        open_time = request.POST.get("open_time")
        close_time = request.POST.get("close_time")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        map = request.POST.get("map")
        short_name = request.POST.get("short_name")

        # type1 = Travel_types.objects.get(type_id = id).name
        # print(type1)

        places = Places(
            place_id = id,
            district = city,
            type_place = type,
            price = price,
            rating = rating,
            dest_name = name,
            img1 = img1,
            img2 = img2,
            img3 = img3,
            img4 = img4,
            img5 = img5,
            desc = description,
            address = address,
            open_time = open_time,
            close_time = close_time,
            email = email,
            phone = phone,
            place_map = map,
            place_name_short = short_name
        )

        places.save()
        return redirect('/admin-home/places-list')

    return render(request, 'places-list.html')
    
def delete_place(request, id):
    places = Places.objects.filter(place_id = id).delete()
    
    # context = {
    #     dess: 'dess'
    # }

    return redirect('/admin-home/places-list')

def foods_list(request):
    foods = Specialties.objects.all()
    types = Specialties_types.objects.all()

    context = {'foods': foods, 'types': types}
    return render(request, 'foods-list.html', context)

def add_food(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        address = request.POST.get("address")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        img3 = request.POST.get("img3")
        description = request.POST.get("description")
        type = request.POST.get("type_spec")

        foods = Specialties(
           spec_name = name,
           address = address,
           img1 = img1,
           img2 = img2,
           img3 = img3,
           desc1 = description,
           type_spec = type 
        )

        foods.save()
        return redirect('foods-list')

    return render(request, 'foods-list.html')

def edit_food(request):
    foods = Specialties.objects.all()

    context = {
        'foods': foods,
    }
    return redirect(request, 'foods-list.html', context)

def update_food(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        address = request.POST.get("address")
        img1 = request.POST.get("img1")
        img2 = request.POST.get("img2")
        img3 = request.POST.get("img3")
        description = request.POST.get("description")
        type = request.POST.get("type_spec")

        foods = Specialties(
            spec_id = id,
            spec_name = name,
            address = address,
            img1 = img1,
            img2 = img2,
            img3 = img3,
            desc1 = description,
            type_spec = type 
        )

        foods.save()
        return redirect('/admin-home/foods-list')

    return render(request, 'foods-list.html')
    
def delete_food(request, id):
    foods = Specialties.objects.filter(spec_id = id).delete()

    return redirect('/admin-home/foods-list')

def bookings(request):
    books = pessanger_detail.objects.all()

    context = {'books': books}

    return render(request, 'bookings.html', context)

def delete_book(request, id):
    foods = pessanger_detail.objects.filter(Trip_id = id).delete()

    return redirect('/admin-home/bookings')

def type_places(request):
    type_places = Travel_types.objects.all()
    # types = Specialties_types.objects.all()

    context = {'type_places': type_places}
    return render(request, 'type-places.html', context)

def add_type_place(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        img = request.POST.get("img")
        code_name = request.POST.get("code_name")

        type_places = Travel_types(
           name = name,
           img = img,
           code_name = code_name
        )

        type_places.save()
        return redirect('type-places')

    return render(request, 'type-places.html')

def edit_type_place(request):
    type_places = Travel_types.objects.all()

    context = {
        'type_places': type_places,
    }
    return redirect(request, 'type-places.html', context)

def update_type_place(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        img = request.POST.get("img")
        code_name = request.POST.get("code_name")

        type_places = Travel_types(
            type_id = id,
            name = name,
            img = img,
            code_name = code_name
        )

        type_places.save()
        return redirect('/admin-home/type-places')

    return render(request, 'type-places.html')
    
def delete_type_place(request, id):
    type_places = Travel_types.objects.filter(type_id = id).delete()

    return redirect('/admin-home/type-places')

##### Type foods business #####
def type_foods_business(request):
    type_foods = Specialties_types.objects.all()
    # types = Specialties_types.objects.all()

    context = {'type_foods': type_foods}
    return render(request, 'type-foods-business.html', context)

def add_type_food_business(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        img = request.POST.get("img")

        type_foods = Specialties_types(
           name = name,
           img = img,
        )

        type_foods.save()
        return redirect('type-foods-business')

    return render(request, 'type-foods-business.html')

def edit_type_food_business(request):
    type_foods = Specialties_types.objects.all()

    context = {
        'type_foods': type_foods,
    }
    return redirect(request, 'type-foods-business.html', context)

def update_type_food_business(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        img = request.POST.get("img")

        type_foods = Specialties_types(
            type_id = id,
            name = name,
            img = img,
        )

        type_foods.save()
        return redirect('/admin-home/type-foods-business')

    return render(request, 'type-foods-business.html')
    
def delete_type_food_business(request, id):
    type_foods = Specialties_types.objects.filter(type_id = id).delete()

    return redirect('/admin-home/type-foods-business')