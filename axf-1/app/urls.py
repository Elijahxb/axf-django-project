

from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^regist/', views.regist, name='regist'),
    url(r'^logout/', views.logout, name='logout'),

]
