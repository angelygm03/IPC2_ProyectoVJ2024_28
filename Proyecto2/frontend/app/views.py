from django.shortcuts import render
import requests
from .forms import LoginForm
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

endpoint = 'http://127.0.0.1:5000/'

contexto = {
    'user':None,
    'contenido_archivo':None,
    'binario_xml':None
}


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def singin(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                #obtenemos los datos del formulario
                iduser = form.cleaned_data['iduser']
                password = form.cleaned_data['password']

                #PETICION AL BACKEND
                #ENDPOINT- URL
                url = endpoint + 'login'
                #DATA A ENVIAR
                data = {
                    'id': iduser,
                    'password': password
                }

                #convertimos los datos a json
                json_data = json.dumps(data)

                #HEADERS
                headers = {
                    'Content-Type': 'application/json'
                }

                #llamamos a la peticion backend
                response = requests.post(url, data=json_data, headers=headers)
                respuesta = response.json()
                if response.status_code == 200:
                    rol = int(respuesta['role'])
                    contexto['user'] = iduser
                    pagina_redireccion = None
                    #IR A ADMIN
                    if rol == 1:
                        #si yo quiero almacenar el usuario en cache
                        #cache.set('id_user', iduser, timeout=None)
                        #si yo quiero almacenar el usuario en cookies
                        pagina_redireccion = redirect('administrador')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion
                    elif rol == 2:
                        #si yo quiero almacenar el usuario en cache
                        #cache.set('id_user', iduser, timeout=None)
                        #si yo quiero almacenar el usuario en cookies
                        pagina_redireccion = redirect('usuario')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion


    except:
        return render(request, 'login.html')

def adminView(request):
    return render(request, 'admin.html')

def userView(request):
    return render(request, 'user.html')

def admincarga(request):
    ctx = {
        'title':'Carga Masiva'
    }
    return render(request, 'uploadFiles.html', ctx)

#def index(request):
#    response = requests.get(endpoint + 'verProductos')
#    productos = response.json()
#    context = {
#        'productos': productos
#   }
#    return render(request, 'index.html', context)

