from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.utils import timezone
import datetime

# Create your models here.
# class Users(models.Model):
#     name 

class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=2)

class Detailed_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=20)
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.CharField(default='5', max_length=10)
    dest_name = models.CharField(max_length=25)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    day1= models.CharField(max_length=200)
    day2 = models.CharField(max_length=200)
    day3 = models.CharField(max_length=200)
    day4 = models.CharField(max_length=200)
    day5 = models.CharField(max_length=200)
    day6 = models.CharField(max_length=200)
    num_bookings = models.IntegerField(default=1)
    trip_date = models.CharField(default='2022-01-30', max_length=19)

class pessanger_detail(models.Model):
    Trip_id = models.AutoField(primary_key=True)
    Trip_same_id = models.IntegerField(default=1)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    age = models.IntegerField(default=10)
    username = models.CharField(max_length=10)
    Trip_date = models.DateField()
    payment = models.IntegerField(default=50)
    city = models.CharField(max_length=20)
    pay_done = models.IntegerField(default=0)

class Cards(models.Model):
    Card_number = models.CharField(primary_key=True, max_length=17)
    Ex_month = models.CharField(max_length=2)
    Ex_Year = models.CharField(max_length=2)
    CVV = models.CharField(max_length=3)
    Balance = models.CharField(max_length=8)
    email=models.EmailField(max_length=50,default='thanhchau2279@gmail.com')
    #rambarodavala21@gmail.com

class NetBanking(models.Model):
    Username = models.CharField(primary_key=True, max_length=16)
    Password = models.CharField(max_length=14)
    Bank=models.CharField(max_length=25)
    Balance = models.CharField(max_length=9)


class Transactions(models.Model):
    Transactions_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    Trip_same_id = models.IntegerField(default=1)
    Amount = models.CharField(max_length=8)
    Status = models.CharField(default="Failed", max_length=15)
    Payment_method = models.CharField(blank=True, max_length=15)
    Date_Time = models.CharField(default=timezone.now(), max_length=19)

class Slide(models.Model):
    slide_id = models.AutoField(primary_key=True)
    slide_image = models.ImageField(upload_to='pics')

class Places(models.Model):
    place_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=20)
    price = models.IntegerField(default=20000)
    rating = models.CharField(default='5', max_length=10)
    dest_name = models.CharField(max_length=300)
    place_name_short = models.CharField(max_length=100, default='culaocham')
    address = models.CharField(max_length=100)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    img3 = models.ImageField(upload_to='pics')
    img4 = models.ImageField(upload_to='pics')
    img5 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    type_place = models.IntegerField(default=1)
    open_time = models.CharField(max_length=10, default='7:00')
    close_time = models.CharField(max_length=10, default='18:00')
    email = models.EmailField(max_length=50, default='thanhchau2279@gmail.com')
    phone = models.IntegerField(default='0917725514')
    place_map = models.CharField(max_length=300, default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3837.1550019355527!2d108.33532111418964!3d15.900948448150865!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31420de155207241%3A0xb084a84384f41fbf!2zTMOgbmcgUmF1IFRyw6AgUXXhur8!5e0!3m2!1svi!2s!4v1671057337843!5m2!1svi!2s') 

class Travel_types(models.Model):
    type_id =  models.AutoField(primary_key=True)
    code_name = models.CharField(max_length=5)
    name = models.CharField(max_length=30) 
    img = models.ImageField(upload_to='pics')

class Specialties(models.Model):
    spec_id = models.AutoField(primary_key=True)
    spec_name = models.CharField(max_length=100, default='Mỳ Quảng')
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    img3 = models.ImageField(upload_to='pics')
    type_spec = models.IntegerField(default=1)
    desc1 = models.TextField()
    desc2 = models.TextField()
    address = models.CharField(max_length=100)

class Specialties_types(models.Model):
    type_id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=30) 
    img = models.ImageField(upload_to='pics')

# class Myrating(models.Model):
#     rating_id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField(default=1)
#     tour_id = models.IntegerField(default=1)
#     rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

class Myrating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tour = models.ForeignKey(Detailed_desc, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    comment = models.CharField(max_length=200, default="Good!!!")
    time_rate = models.DateField(default=timezone.now())

class PlaceRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    place = models.ForeignKey(Places, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    comment = models.CharField(max_length=200)
    time_rate = models.DateTimeField(auto_now_add=True)

class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Detailed_desc, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)