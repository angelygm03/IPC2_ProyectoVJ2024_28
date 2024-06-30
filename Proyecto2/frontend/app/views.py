from django.shortcuts import render
import requests
from django.contrib import messages
from .forms import LoginForm, FileForm, AddCartForm
import json
from django.http import JsonResponse
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # obtenemos los datos del formulario
            iduser = form.cleaned_data['iduser']
            password = form.cleaned_data['password']

            # PETICION AL BACKEND
            # ENDPOINT- URL
            url = endpoint + 'login'
            # DATA A ENVIAR
            data = {
                'id': iduser,
                'password': password
            }

            # convertimos los datos a json
            json_data = json.dumps(data)

            # HEADERS
            headers = {
                'Content-Type': 'application/json'
            }

            # llamamos a la peticion backend
            response = requests.post(url, data=json_data, headers=headers)
            respuesta = response.json()
            if response.status_code == 200:
                rol = int(respuesta['role'])
                contexto['user'] = iduser
                pagina_redireccion = None
                # IR A ADMIN
                if rol == 1:
                    pagina_redireccion = redirect('administrador')
                    pagina_redireccion.set_cookie('id_user', iduser)
                    return pagina_redireccion
                elif rol == 2:
                    pagina_redireccion = redirect('usuario')
                    pagina_redireccion.set_cookie('id_user', iduser)
                    return pagina_redireccion
                else:
                    messages.error(request, 'Rol no válido')
            else:
                messages.error(request, 'Credenciales incorrectas')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def adminView(request):
    return render(request, 'admin.html')


def userView(request):
    return render(request, 'user.html')


def admincarga(request):
    ctx = {
        'title':'Carga Masiva'
    }
    return render(request, 'uploadFiles.html', ctx)

def cargarXML(request):
    ctx = {
        'contenido_archivo':None
    }
    try:
        if request.method == 'POST':
            #obtenemos el formulario
            form = FileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                #obtenemos el archivo
                archivo = request.FILES['file']
                #guardamos el binario
                xml = archivo.read()
                xml_decodificado = xml.decode('utf-8')
                #guardamos el contenido del archivo
                contexto['binario_xml'] = xml
                contexto['contenido_archivo'] = xml_decodificado
                ctx['contenido_archivo'] = xml_decodificado
                return render(request, 'uploadFiles.html', ctx)
    except:
        return render(request, 'uploadFiles.html')

def enviarUsuarios(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'uploadFiles.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'cargaUsuarios'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'uploadFiles.html', contexto)
    except:
        return render(request, 'uploadFiles.html')


def enviarProductos(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'uploadFiles.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'cargaProductos'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'uploadFiles.html', contexto)
    except:
        return render(request, 'uploadFiles.html')


def enviarEmpleados(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'uploadFiles.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'cargaEmpleados'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'uploadFiles.html', contexto)
    except:
        return render(request, 'uploadFiles.html')

def verProductos(request):
    response = requests.get(endpoint + 'verProductos')
    productos = response.json()
    context = {
        'productos': productos
    }
    return render(request, 'mostrarProductos.html', context)

def comprar(request):
    response = requests.get(endpoint + 'verProductos')
    productos = response.json()
    context = {
        'productos': productos
    }
    return render(request, 'user.html', context)

def añadirCarrito(request):
    try:
        if request.method == 'POST':
            form = AddCartForm(request.POST)
            if form.is_valid():
                user_id = form.cleaned_data['user_id']
                product_id = form.cleaned_data['product_id']
                cantidad = request.POST.get('cantidad', 1)  # Obtener la cantidad del formulario
                print(f"Datos enviados al backend: user_id={user_id}, product_id={product_id}, cantidad={cantidad}")  # Print para depuración
                # PETICION AL BACKEND
                url = endpoint + 'añadirCarrito'
                data = {
                    'user_id': user_id,
                    'product_id': product_id,
                    'cantidad': int(cantidad)  # Asegurarse de enviar la cantidad como entero
                }
                json_data = json.dumps(data)
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, data=json_data, headers=headers)
                print(f"Respuesta del backend: {response.status_code}, {response.json()}")  # Print para depuración
                if response.status_code == 200:
                    mensaje = response.json()
                    messages.success(request, mensaje['message'])
                else:
                    mensaje = response.json()
                    messages.error(request, mensaje['message'])
            else:
                messages.error(request, 'Formulario no válido')
            return redirect('comprar')
    except Exception as e:
        return redirect('comprar')
    
def Carrito(request):
    try:
        user_id = request.COOKIES.get('id_user')
        url = endpoint + 'generarXMLCarrito'
        params = {
            'user_id': user_id
        }
        response = requests.get(url, params=params)
        xml_content = response.text 
        context = {
            'xml_content': xml_content
        }
        return render(request, 'carrito.html', context)
    except Exception as e:
        return redirect('comprar')


def confirmarCompra(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            if not user_id:
                messages.error(request, 'User ID is required')
                return redirect('carrito')

            url = endpoint + 'confirmarCompra'
            data = {'user_id': user_id}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                mensaje = response.json()
                messages.success(request, mensaje['message'])
            else:
                mensaje = response.json()
                messages.error(request, mensaje['message'])

            return redirect('carrito')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('carrito')

def generar_reporte_compras(request):
    try:
        url = endpoint + 'generarReporte'
        response = requests.get(url)
        if response.status_code == 200:
            xml_content = response.text
            context = {'xml_content': xml_content}
            return render(request, 'reportes.html', context)
        else:
            messages.error(request, 'Error al generar el reporte')
            return redirect('administrador')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('administrador')

def enviarActividades(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'uploadFiles.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'cargaActividades'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'uploadFiles.html', contexto)
    except:
        return render(request, 'uploadFiles.html')

def verActividades(request):
    try:
        url = endpoint + 'generarXMLActividadesHoy'
        response = requests.get(url)
        
        if response.status_code == 200:
            xml_content = response.text
            context = {'xml_content': xml_content}
            return render(request, 'actividades.html', context)
        else:
            messages.error(request, 'Error al obtener las actividades del día')
            return redirect('administrador')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('administrador')

def estadisticas(request):
    return render(request, 'estadisticas.html')

def top3Categorias(request):
    try:
        url = endpoint + 'top3Categorias'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            messages.error(request, 'Error al obtener las categorías')
            return redirect('estadisticas')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('estadisticas')

def top3Productos(request):
    try:
        url = endpoint + 'top3Productos'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            messages.error(request, 'Error al obtener los productos')
            return redirect('estadisticas')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('estadisticas')

def ayuda(request):
    return render(request, 'ayuda.html')

def logout(request):
    response = redirect('login')
    response.delete_cookie('id_user')
    return response