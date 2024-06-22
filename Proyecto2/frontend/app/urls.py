from django.urls import path
from . import views

#aqui van todas las urls de la pagina /login, etc
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('administrador/', views.adminView, name='administrador'),
    path('usuario/', views.userView, name='usuario'),
    path('singin/', views.singin, name='singin'),
    path('upload/', views.admincarga, name='upload'),
]