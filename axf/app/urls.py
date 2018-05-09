

from django.conf.urls import url
from app import views
from rest_framework.routers import SimpleRouter

#
# router = SimpleRouter()
# router.register(r'goods', views.GoodsInfo)

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    # 注册
    url(r'^regist/', views.regist, name='regist'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^market/$', views.user_market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.market_params, name='marketparams'),

    url(r'^wait_payed/', views.wait_payed, name='wait_payed'),
    url(r'^wait_get', views.wait_get, name='wait_get'),

    # 添加购物车
    url(r'^addgoods/', views.add_goods, name='addgoods'),
    url(r'^subgoods/', views.sub_goods, name='subgoods'),
    # 购物车
    url(r'cart/', views.cart, name='cart'),
    # 修改购物车商品的选择
    url(r'^changecartselect/', views.user_change_select, name='change_select'),
]

# urlpatterns += router.urls
