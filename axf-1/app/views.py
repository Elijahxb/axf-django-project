import random
import time
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from app.models import MainMustBuy, MainNav, MainShow, MainShop, MainWheel, UserModel
from django.contrib import auth
# Create your views here.


def home(request):
    if request.method == 'GET':
        mustbuys = MainMustBuy.objects.all()
        mainnavs = MainNav.objects.all()
        mainwheels = MainWheel.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()
        data = {

            'mustbuys': mustbuys,
            'mainnavs': mainnavs,
            'manwheels': mainwheels,
            'mainshows': mainshows,
            'mainshops': mainshops

        }

        return render(request, 'home/home.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        users = UserModel.objects.filter(username=user, is_delete=0).exists()
        if users:
            User = UserModel.objects.get(username=user)
            if check_password(password, User.password):
                s = '1234567890qwertyuiopasdfghjklzxcvbnm'
                ticket = ''
                for i in range(15):
                    ticket += random.choice(s)
                ticket += str(int(time.time()))
                User.ticket = ticket
                User.save()
                response = HttpResponseRedirect('/axf/home/')
                response.set_cookie('ticket', ticket, max_age=3000)
                return response
            else:
                return render(request, 'user/user_login.html')
        else:
            return render(request, 'user/user_login.html')


def regist(request):

    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        UserModel.objects.create(username=name,
                                 password=password,
                                 email=email,
                                 icon=icon)

        return HttpResponseRedirect('/axf/login')


def logout(request):

    if request.method == 'GET':
        response = HttpResponse()
        response.delete_cookie('ticket')
        return HttpResponseRedirect('/axf/login/')
