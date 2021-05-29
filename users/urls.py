from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^register/$', views.registerPage, name='register'),
    url(r'^user_login/$', views.loginPage, name='login'),
]
