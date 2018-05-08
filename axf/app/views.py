import random
from datetime import datetime, timedelta
import time
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from app.models import MainMustBuy, MainNav, MainShow, MainShop, MainWheel, UserModel, UserTicket

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
        # now_time = datetime.date.today()
        out_time = datetime.now() + timedelta(days=1)
        if users:
            User = UserModel.objects.get(username=user)
            if check_password(password, User.password):
                s = '1234567890qwertyuiopasdfghjklzxcvbnm'
                ticket = ''
                for i in range(15):
                    ticket += random.choice(s)
                ticket += str(int(time.time()))
                isexists = UserTicket.objects.filter(user=User.id).exists()
                if isexists:
                    Ticket = UserTicket.objects.get(user=User.id)
                    Ticket.ticket = ticket
                    Ticket.save()
                else:
                    UserTicket.objects.create(
                        user=User,
                        ticket=ticket,
                        out_time=out_time
                    )

                response = HttpResponseRedirect('/axf/mine/')
                response.set_cookie('ticket', ticket, expires=out_time)
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
        # 删除ticket
        response = HttpResponseRedirect(reverse('axf:home'))
        response.delete_cookie('ticket')

        ticket = request.COOKIES.get('ticket')
        UserTicket.objects.filter(ticket=ticket).delete()
        return response


def mine(request):
    if request.method == 'GET':
        user = request.user

        if user.id:
            orders = user.ordermodel_set.all()

            wait_pay, payed = 0, 0
            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
            data = {
                'wait_pay': wait_pay,
                'payed': payed
            }
            # data['wait_pay']: wait_pay
            # data['payed']: payed

        return render(request, 'mine/mine.html', data)


def cart(request):
    if request.method == 'GET':
        return render(request, 'cart/cart.html')


def market(request):
    if request.method == 'GET':
        return render(request, 'market/market.html')