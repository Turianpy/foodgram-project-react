from django.urls import path

from . import views

app_name = 'authentication'


urlpatterns = [
    path('token/login/', views.login, name='login'),
    path('token/logout/', views.logout, name='logout')
]
