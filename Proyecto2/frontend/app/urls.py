from django.urls import path
from . import views

#aqui van todas las urls de la pagina /login, etc
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('administrador/', views.admincarga, name='administrador'),
    path('usuario/', views.userView, name='usuario'),
    path('singin/', views.singin, name='singin'),
    path('upload/', views.admincarga, name='upload'),
    path('cargaxml/', views.cargarXML, name='cargaxml'),
    path('xmlusuarios/', views.enviarUsuarios, name='xmlusuarios'),
    path('xmlproductos/', views.enviarProductos, name='xmlproductos'),
    path('xmlempleados/', views.enviarEmpleados, name='xmlempleados'),
    path('verProductos/', views.verProductos, name='verProductos'),
    path('comprar/', views.comprar, name='comprar'),
    path('añadirCarrito/', views.añadirCarrito, name='añadirCarrito'),
]