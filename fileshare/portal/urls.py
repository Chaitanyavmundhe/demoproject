# portal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',          views.login_view,    name='login'),
    path('home/',     views.home_view,     name='home'),
    path('logout/',   views.logout_view,   name='logout'),
    path('register/', views.register_view, name='register'),
    path('upload/',   views.upload_view,   name='upload'),
]