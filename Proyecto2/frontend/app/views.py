from django.shortcuts import render
import requests

# Create your views here.

endpoint = 'http://127.0.0.1:5000/'

def home(request):
    response = requests.get(endpoint + 'verProductos')
    productos = response.json()
    context = {
        'productos': productos
    }
    return render(request, 'index.html', context)