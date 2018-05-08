

from django.conf.urls import url
from app import views


urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    # 注册
    url(r'^regist/', views.regist, name='regist'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^market/', views.market, name='market'),

]


