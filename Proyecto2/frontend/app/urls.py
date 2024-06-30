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
    path('xmlactividades/', views.enviarActividades, name='xmlactividades'),
    path('verProductos/', views.verProductos, name='verProductos'),
    path('comprar/', views.comprar, name='comprar'),
    path('añadirCarrito/', views.añadirCarrito, name='añadirCarrito'),
    path('carrito/', views.Carrito, name='carrito'),
    path('confirmarCompra/', views.confirmarCompra, name='confirmarCompra'),
    path('generarReporte/', views.generar_reporte_compras, name='generarReporte'),
    path('verActividades/', views.verActividades, name='verActividades'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('top3Categorias/', views.top3Categorias, name='top3Categorias'),
    path('top3Productos/', views.top3Productos, name='top3Productos'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('logout/', views.logout, name='logout'),
]
