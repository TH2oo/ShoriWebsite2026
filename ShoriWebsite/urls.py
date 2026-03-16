from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('form/', views.application_view, name='form'),
    path('profil/', views.profil_view, name='profil')
]