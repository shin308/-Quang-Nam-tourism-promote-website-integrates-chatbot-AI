from django.shortcuts import render
from .models import Destination
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import Transactions
from .models import NetBanking
from .models import Places
from .models import Travel_types
from .models import Specialties_types
from .models import Specialties
from .models import Myrating
from .models import PlaceRating
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
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
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
# from flask import request
from travello.chatbot_run import chatbot_response
from scrape import scrape_data
from django.http import HttpResponseRedirect, Http404
from django.db.models import Case, When
import pandas as pd

check_wikipedia1 = ['what', 'is']
check_wikipedia2 = ['who', 'is']
check_wikihow = ['how', 'to']


import random

#  __lte=      is eqivelent to lessthan or euivelent
#    table.all().filter().exclude().filer()   for two filters and one excluding condition
# Create your views here.

def index(request):
    dests = Destination.objects.all()
    total_data = Detailed_desc.objects.filter(rating=5.0).count()
    ratings = Myrating.objects.filter(rating=5.0)[:4]
    #dest1 = []
    #j=0
    # for i in range(6):
        #j=j+2
    temp = Detailed_desc.objects.filter(rating=5.0)[:6]
        # dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : temp, 'total_data': total_data, 'ratings': ratings})

def load_more_tours(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Detailed_desc.objects.filter(rating=5.0)[offset:offset+limit]
        # dest1.append(temp)
    t = render_to_string('ajax/tours-list.html', {'data': data})
    return JsonResponse({'data':t})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)
                user.save()
                print('user Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        if user is not None:
            if request.user.last_name == 'admin':
                messages.info(request, 'Sucessfully Logged in')
                email = request.user.email
                print(email)
                content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
                # send_mail('Alert for Login', content
                #           , 'travellotours89@gmail.com', [email], fail_silently=True)
                dests = Destination.objects.all()
                return render(request, 'web_admin/admin_home.html',{'dests':dests})
            else:
                messages.info(request, 'Sucessfully Logged in')
                email = request.user.email
                print(email)
                content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
                # send_mail('Alert for Login', content
                #           , 'travellotours89@gmail.com', [email], fail_silently=True)
                dests = Destination.objects.all()
                return render(request, 'index.html',{'dests':dests}) and redirect('/')
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')

def all_users(request):
    return render(request, 'web_admin/all_user.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def blog(request):
    return render(request, 'blog.html')

def about(request):
    return render(request, 'about.html')

# @login_required(login_url='login')
def destination_list(request,city_name):
    total_data = Detailed_desc.objects.all().filter(country=city_name).count()
    dests = Detailed_desc.objects.all().filter(country=city_name)[:2]
    dest_name = city_name
    return render(request,'travel_destination.html',{'dests': dests, 'dest_name': dest_name, 'total_data': total_data})

def load_more_private_tours(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    tour_name = request.GET['name']
    #print(tour_name)
    data = Detailed_desc.objects.all().filter(country = tour_name)[offset:offset+limit]
        # dest1.append(temp)
    t = render_to_string('ajax/private-tours-list.html', {'data': data})
    return JsonResponse({'data':t})

def destination_details(request, tour_id):
    # dest = Detailed_desc.objects.get(dest_name=city_name)
    dest = get_object_or_404(Detailed_desc, dest_id=tour_id)
    dest1 = Detailed_desc.objects.get(dest_id = tour_id)

    price = dest.price
    city_name = dest.dest_name
    trip_date = dest.trip_date
    # country = dest.country
    # img1 = dest.img1
    # img2 = dest.img2
    # desc = dest.desc
    # day1 = dest.day1
    # day2 = dest.day2
    # day3 = dest.day3
    # day4 = dest.day4
    # day5 = dest.day5
    # day6 = dest.day6
    # rating_tour = dest.rating
    # number_bookings = dest.num_bookings

    request.session['price'] = price
    request.session['city'] = city_name
    request.session['trip_date'] = trip_date
    # request.session['country'] = city_name

    tour = Detailed_desc.objects.get(dest_id=tour_id)
    ratings = Myrating.objects.filter(tour_id=tour_id)
    #tours = get_object_or_404(Detailed_desc, dest_id=tour_id)

    if request.method == "POST":
        # For rating
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            rate = request.POST['rating']
            comment = request.POST['comment']
            time_rate = datetime.now().date()
            if Myrating.objects.all().values().filter(tour_id=tour_id,user_id=request.user.id):
                Myrating.objects.all().values().filter(tour_id=tour_id,user_id=request.user.id).update(rating=rate)
                Myrating.objects.all().values().filter(tour_id=tour_id,user_id=request.user.id).update(comment=comment)
                Myrating.objects.all().values().filter(tour_id=tour_id,user_id=request.user.id).update(time_rate=time_rate)
            else:
                q=Myrating(user_id=request.user.id,tour_id=tour_id,rating=rate, comment=comment)
                q.save()
                
            allRating = (float(dest1.rating) + int(rate))/2
            dest1.rating = str(round(allRating, 1))
            print(dest1.rating)
            dest1.save(update_fields=['rating'])
            dest1.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user_id=request.user.id).values())

    # To display ratings in the movie detail page
    tour_rating = 0
    rate_flag = False
    for each in out:
        if each['tour_id'] == tour_id:
            tour_rating = each['rating']
            rate_flag = True
            break

    context = {'dest':dest,'tour_rating':tour_rating,'rate_flag':rate_flag, 'ratings': ratings, 'dest1': dest1}

    return render(request,'destination_details.html', context)

def search(request):
    try:
        place1 = request.POST['place']
        print(place1)
        dests = Detailed_desc.objects.filter(country__icontains=place1)
        print(place1)
        return render(request, 'travel_destination.html', {'dests': dests})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            trip_date = request.session['trip_date']
            temp_date = datetime.strptime(trip_date, "%Y-%m-%d").date()
            print(type(trip_date))
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=1)
            #trip_same_id
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(trip_date)
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(trip_date, "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total
            request.session['tour_name'] = city
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'GST': GST, 'final_total': final_total,'city': city })
    else:
        formset = KeyValueFormSet()

        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, })


def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})

@login_required(login_url='login')
def card_payment(request):
    card_no = request.POST.get('card_number')
    pay_method = 'Debit card'
    MM = request.POST.get('MM')
    YY = request.POST.get('YY')
    CVV = request.POST.get('cvv')

    request.session['dcard'] = card_no
    # try:
    balance = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).Balance
    request.session['total_balance'] = balance
    mail1 = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).email

    if int(balance) >= int(request.session['pay_amount']):
        # print("if ma gayu")
        rno = random.randint(100000, 999999)
        request.session['OTP'] = rno

        amt = request.session['pay_amount']
        username = request.user.get_username()
        print(username)
        user = User.objects.get(username=username)
        mail_id = user.email
        print([mail_id])
        msg = 'Your OTP For Payment of ₹' + str(amt) + ' is ' + str(rno)
        # print(msg)
        # print([mail_id])
        # print(amt)
        send_mail('OTP for Debit card Payment',
                    msg,
                    'vqnhat.18it3@vku.udn.vn',
                    [mail_id,],
                    fail_silently=False)
        return render(request, 'OTP.html')
    return render(request, 'wrongdata.html')


    # except:
    #      return render(request, 'wrongdata.html')

@login_required(login_url='login')
def net_payment(request):
    username = request.POST['cardNumber']
    Password1 = request.POST['pass']
    Bank_name = request.POST['banks']
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Net Banking'
    tour_name = request.session['tour_name']
    tours = Detailed_desc.objects.get(dest_name = tour_name)
    try:
        r = NetBanking.objects.get(Username=username, Password=Password1,Bank=Bank_name)
        balance = r.Balance
        request.session['total_balance'] = balance
        if int(balance) >= int(request.session['pay_amount']):
            total_balance = int(request.session['total_balance'])
            rem_balance = int(total_balance - int(request.session["pay_amount"]))
            r.Balance = rem_balance
            r.save(update_fields=['Balance'])
            r.save()
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
            t.save()
            z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
            for obj in z:
                obj.pay_done = 1
                obj.save(update_fields=['pay_done'])
                obj.save()
                print(obj.pay_done)
            tours.num_bookings -= 1
            tours.save(update_fields=['num_bookings'])
            tours.save()
            print(tours.num_bookings)
            return render(request, 'confirmetion_page.html')
        else:
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
            t.save()
            return render(request, 'wrongdata.html')
    except :
        return render(request, 'wrongdata.html')

@login_required(login_url='login')
def otp_verification(request):
    otp1 = int(request.POST.get('otp'))
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    tour_name = request.session['tour_name']
    pay_method = 'Debit card'
    tours = Detailed_desc.objects.get(dest_name = tour_name)
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance-int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
        t.save()
        z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
        for obj in z:
            obj.pay_done = 1
            obj.save(update_fields=['pay_done'])
            obj.save()
            print(obj.pay_done)
        tours.num_bookings -= 1
        tours.save(update_fields=['num_bookings'])
        tours.save()
        print(tours.num_bookings)
        return render(request, 'confirmetion_page.html')
    else:
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
        t.save()
        return render(request, 'wrong_OTP.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)
    
@csrf_exempt
def get_bot_response(request):
    user_request =  request.GET['msg']
    user_request = user_request.lower()
    if len(user_request.split(" ")) > 1:
        check_search = user_request.split(" ")[0]
        if check_search == 'google':
            user_request = user_request.replace("google","")
            user_request = user_request.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            check_query = user_request.split(" ")[1]
            check_text = user_request.split(" ")[1:3]
            if check_text == check_wikipedia1 or check_text == check_wikipedia2:
                response = scrape_data(user_request, "wikipedia")
            elif check_text == check_wikihow:
                response = scrape_data(user_request, "wikihow")
            elif check_query == "nearby":
                response = scrape_data(user_request, "nearby")
            else:
                response = scrape_data(user_request, "")
                
        else:
            response = chatbot_response(user_request)                

    else:
        response = chatbot_response(user_request)
    
    return HttpResponse(response)

def check_places_VH(request):
    places_vh = Places.objects.filter(type_place = 'VH')

    return render(request, 'places.html', {'places': places_vh})

def check_places_TN(request):
    places_tn = Places.objects.filter(type_place = 'TN')

    return render(request, 'places.html', {'places': places_tn})

def check_places_LQ(request):
    places_lq = Places.objects.filter(type_place = 'LQ')

    return render(request, 'places.html', {'places': places_lq})

def check_places_NN(request):
    places_nn = Places.objects.filter(type_place = 'NN')

    return render(request, 'places.html', {'places': places_nn})

# To get similar places based on user rating
def get_similar(place_name,rating,corrMatrix):
    similar_ratings = corrMatrix[place_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

def places(request):
    places = Places.objects.all()
    types = Travel_types.objects.all()
    # places1 = []
    # j=0
    # for i in range(6):
    #     j=j+2
    #     temp = Places.objects.get(place_id=j)
    #     places1.append(temp)

    ### Places recommendation for user
    place_rating=pd.DataFrame(list(PlaceRating.objects.all().values()))

    new_user=place_rating.user_id.unique().shape[0]
    current_user_id= request.user.id
	# if new user not rated any place
    if request.user.is_authenticated:
        if current_user_id > new_user:
            place=Places.objects.get(place_id=5)
            q=PlaceRating(user=request.user,place=place,comment='good!!!',rating=5)
            q.save()


        userRatings = place_rating.pivot_table(index=['user_id'],columns=['place_id'],values='rating')
        userRatings = userRatings.fillna(0,axis=1)
        corrMatrix = userRatings.corr(method='pearson')

        user = pd.DataFrame(list(PlaceRating.objects.filter(user=request.user).values())).drop(['user_id','rating_id'],axis=1)
        user_filtered = [tuple(x) for x in user.values]
        place_id_watched = [each[0] for each in user_filtered]

        #print(user_filtered)

        similar_movies = pd.DataFrame()
        for place,rating,*z in user_filtered:
            similar_movies = similar_movies.append(get_similar(place,rating,corrMatrix),ignore_index = True)

        places_id = list(similar_movies.sum().sort_values(ascending=False).index)
        places_id_recommend = [each for each in places_id if each not in place_id_watched]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(places_id_recommend)])
        place_list=list(Places.objects.filter(place_id__in = places_id_recommend).order_by(preserved)[:5])

        return render(request, 'places.html',{'places': places, 'types': types, 'place_list': place_list})
    else:
        return render(request, 'places.html',{'places': places, 'types': types})



def specialties(request):
    specialties = Specialties.objects.all()
    types = Specialties_types.objects.all()

    return render(request, 'specialties.html', {'specialties': specialties, 'types': types})

def place_details(request, place_id):
    #place = Places.objects.get(place_id = place_id)
    place = get_object_or_404(Places, place_id=place_id)
    place1 = Places.objects.get(place_id = place_id)

    # price = place.price
    # place_name = place.dest_name
    # country = place.district
    # address = place.address
    # img1 = dest.img1
    # img2 = dest.img2
    # desc = dest.desc
    # day1 = dest.day1
    # day2 = dest.day2
    # day3 = dest.day3
    # day4 = dest.day4
    # day5 = dest.day5
    # day6 = dest.day6
    # rating_tour = dest.rating
    # number_bookings = dest.num_bookings

    # request.session['price'] = price
    # request.session['place_name'] = place_name
    # request.session['country'] = city_name

    #tour = Detailed_desc.objects.get(dest_id=tour_id)
    ratings = PlaceRating.objects.filter(place_id=place_id)

    if request.method == "POST":
        # For rating
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            rate = request.POST['rating']
            comment = request.POST['comment']
            time_rate = datetime.now()
            if PlaceRating.objects.all().values().filter(place_id=place_id,user_id=request.user.id):
                PlaceRating.objects.all().values().filter(place_id=place_id,user_id=request.user.id).update(rating=rate)
                PlaceRating.objects.all().values().filter(place_id=place_id,user_id=request.user.id).update(comment=comment)
                PlaceRating.objects.all().values().filter(place_id=place_id,user_id=request.user.id).update(time_rate=time_rate)
            else:
                q=PlaceRating(user_id=request.user.id,place_id=place_id,rating=rate, comment=comment)
                q.save()
            
            allRating = (float(place1.rating) + int(rate))/2
            place1.rating = str(round(allRating, 1))
            print(place1.rating)
            place1.save(update_fields=['rating'])
            place1.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(PlaceRating.objects.filter(user_id=request.user.id).values())

    # To display ratings in the movie detail page
    place_rating = 0
    rate_flag = False
    for each in out:
        if each['place_id'] == place_id:
            place_rating = each['rating']
            rate_flag = True
            break
    context = {'place': place,'place_rating':place_rating,'rate_flag':rate_flag, 'ratings': ratings, 'place1': place1}

    return render(request, 'place_details.html', context)

def specialties_details(request, spec_id):
    spec = Specialties.objects.get(spec_id = spec_id)

    return render(request, 'specialties_detail.html', {'spec': spec})

# Filter data places
def filter_places(request):
    type_places = request.GET.getlist('type_place[]')
    allPlaces = Places.objects.all().order_by('-type_place')
    if len(type_places) > 0:
        allPlaces = allPlaces.filter(type_place__in=type_places).distinct()  

    t = render_to_string('ajax/places-list.html', {'data': allPlaces})
    return JsonResponse({'data': t})

# Filter data specialties
def filter_specialties(request):
    type_specialties = request.GET.getlist('type_spec[]')
    allSpecialties = Specialties.objects.all().order_by('-type_spec')
    if len(type_specialties) > 0:
        allSpecialties = allSpecialties.filter(type_spec__in=type_specialties).distinct()  

    t = render_to_string('ajax/specialties-list.html', {'data': allSpecialties})
    return JsonResponse({'data': t})

# Places Recommendation Algorithm
def recommend(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404


    place_rating=pd.DataFrame(list(PlaceRating.objects.all().values()))

    new_user=place_rating.user_id.unique().shape[0]
    current_user_id= request.user.id
	# if new user not rated any movie
    if current_user_id>new_user:
        place=Places.objects.get(place_id=5)
        q=PlaceRating(user=request.user,place=place,rating=0)
        q.save()


    userRatings = place_rating.pivot_table(index=['user_id'],columns=['place_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(PlaceRating.objects.filter(user=request.user).values())).drop(['user_id','rating_id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    place_id_watched = [each[0] for each in user_filtered]

    #print(user_filtered)

    similar_movies = pd.DataFrame()
    for place,rating,*z in user_filtered:
        similar_movies = similar_movies.append(get_similar(place,rating,corrMatrix),ignore_index = True)

    places_id = list(similar_movies.sum().sort_values(ascending=False).index)
    places_id_recommend = [each for each in places_id if each not in place_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(places_id_recommend)])
    place_list=list(Places.objects.filter(place_id__in = places_id_recommend).order_by(preserved)[:5])

    context = {'place_list': place_list}
    return render(request, 'recommend.html', context)

def tours_list(request):
    tours = Detailed_desc.objects.all()
    types = Destination.objects.all()

    return render(request, 'tours-list.html', {'tours': tours, 'types': types})

# Filter data tours
def filter_tours(request):
    type_tour = request.GET.getlist('country[]')
    allTours = Detailed_desc.objects.all().order_by('-country')
    if len(type_tour) > 0:
        allTours = allTours.filter(country__in=type_tour).distinct()  

    t = render_to_string('ajax/tour-list-filter.html', {'data': allTours})
    return JsonResponse({'data': t})

@csrf_exempt
def user(request , user_id):
    user = User.objects.get(id = user_id)
    if request.method == 'POST':
        old_pass = request.POST['old-pass']
        new_pass = request.POST['new-pass']
        cof_pass = request.POST['cof-new-pass']

        success = user.check_password(old_pass)
        if success:
            if new_pass == cof_pass:
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Đổi mật khẩu thành công')
            else:
                messages.info(request, 'Mật khẩu mới không trùng')
        else:
            messages.info(request, 'Sai mật khẩu cũ')

    context = {'user': user}
    return render(request, 'user.html', context)