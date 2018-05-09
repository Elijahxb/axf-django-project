import random
from datetime import datetime, timedelta
import time
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework import viewsets, mixins
from app.serializers import GoodsSerializer

from app.models import MainMustBuy, MainNav, MainShow, MainShop, MainWheel, UserModel, UserTicket, \
    FoodType, Goods, CartModel

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
        data = {}

        if user and user.id:
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


def user_market(request):
    # if request.method == 'GET':

        return HttpResponseRedirect(reverse('axf:marketparams', args=('104749', '0', '0')))


def market_params(request, typeid, cid, sort_id):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        # 获取商品
        if cid == '0':
            goods_types = Goods.objects.filter(categoryid=typeid)
        else:
            goods_types = Goods.objects.filter(categoryid=typeid,
                                               childcid=cid)

    # 商品分类
        if sort_id == '0':
            pass
        elif sort_id == '1':
            goods_types.order_by('productnum')

        elif sort_id == '2':
            goods_types = goods_types.order_by('-price')
        elif sort_id == '3':
            goods_types = goods_types.order_by('price')

        # 获取分类全部类型
        foodtypes_childnames = FoodType.objects.filter(typeid=typeid).first()
        childtypenames = foodtypes_childnames.childtypenames
        childtypenames_list = childtypenames.split('#')

        child_types_list = []

        for childtypename in childtypenames_list:
            child_types_list.append(childtypename.split(':'))

        data = {'foodtypes': foodtypes,
                'cid': cid,
                'goods_types': goods_types,
                'child_types_list': child_types_list,
                'sort_id': sort_id,
                'typeid': typeid,
                ' foodtypes_childnames': foodtypes_childnames}

        return render(request, 'market/market.html', data)


# def goods(request, typeid):
#     if request.method == 'GET':
#         type_id = FoodType.objects.filter(typeid=typeid)
#         foodtypes = Goods.objects.filter(categoryid=typeid)
#         foodtype = FoodType.objects.all()
#
#         return render(request, 'market/market.html', {'type_id': type_id,
#                                                       'food_type': foodtype,
#                                                       'food_types': foodtypes})


def wait_payed(request):
    if request.method == 'GET':

        return render(request, 'order/order_list_wait_pay.html')


def wait_get(request):
    if request.method == 'GET':

        return render(request, 'order/order_list_payed.html')


def add_goods(request):

    if request.method == 'POST':

        data = {
            'msg': '请求成功',
            'code': '200',
        }
        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            # 获取购物车信息
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果用户选了商品
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                # 如果没选商品，新建商品
                CartModel.objects.create(user=user,
                                         goods_id=goods_id,
                                         c_num=1)
                data['c_num'] = 1

        return JsonResponse(data)


def sub_goods(request):

    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200',
        }

        user = request.user
        goods_id = request.POST.get('goods_id')

        if user and user.id:
            # 查看当前商品是否在购物车中
            user_carts = CartModel.objects.filter(user=user,
                                                  goods_id=goods_id).first()
            # 如果存在则减 1
            if user_carts:
                # 如果商品数量为1，则删除
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num

        return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 如果用户已经登录，则加载购物车的数据
            carts = CartModel.objects.filter(user=user)

            return render(request, 'cart/cart.html', {'carts': carts})

        else:
            return HttpResponseRedirect(reverse('axf:login'))


def user_change_select(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        user = request.user
        data = {
            'code': 200,
            'msg': '请求成功'
        }

        if user and user.id:

            cart = CartModel.objects.filter(pk=cart_id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select
        return JsonResponse(data)
