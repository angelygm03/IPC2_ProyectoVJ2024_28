# lista_doble/lista_doble.py
from .nodo import Nodo
import os
from graphviz import Digraph

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def insertar(self, usuario):
        nuevo = Nodo(usuario)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def buscar_por_id(self, id):
        actual = self.cabeza
        while actual is not None:
            if actual.usuario.id == id:
                return actual.usuario
            actual = actual.siguiente
        return None
    
    def imprimir_usuarios(self):
        actual = self.cabeza
        while actual is not None:
            usuario = actual.usuario
            print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Edad: {usuario.edad}, Email: {usuario.email}, Teléfono: {usuario.telefono}")
            actual = actual.siguiente

    def graficar(self):
        codigo_dot = ''
        ruta_directorio_dot = './reportedot'
        ruta_directorio_img = './Reportes'
        ruta_dot = f'{ruta_directorio_dot}/ListaUsuarios.dot'
        ruta_imagen = f'{ruta_directorio_img}/ListaUsuarios.png'

        # Crear los directorios si no existen
        if not os.path.exists(ruta_directorio_dot):
            os.makedirs(ruta_directorio_dot)
        if not os.path.exists(ruta_directorio_img):
            os.makedirs(ruta_directorio_img)

        archivo = open(ruta_dot, 'w')
        codigo_dot += '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]
  charset=latin1;
'''
        actual = self.cabeza
        contador_nodos = 0
        # Creamos los nodos
        while actual is not None:
            usuario = actual.usuario
            codigo_dot += f'node{contador_nodos} [label = "{{<f1>| ID: {usuario.id} \\n Nombre: {usuario.nombre} \\n Edad: {usuario.edad} \\n Email: {usuario.email} \\n Teléfono: {usuario.telefono} |<f2>}}"];\n'
            contador_nodos += 1
            actual = actual.siguiente

        # Establecemos las relaciones
        actual = self.cabeza
        contador_nodos = 0
        while actual.siguiente is not None:
            # Relaciones de izquierda a derecha
            codigo_dot += f'node{contador_nodos}:f2 -> node{contador_nodos + 1}:f1;\n'
            # Relaciones de derecha a izquierda
            codigo_dot += f'node{contador_nodos + 1}:f1 -> node{contador_nodos}:f2;\n'
            contador_nodos += 1
            actual = actual.siguiente

        codigo_dot += '}'
        archivo.write(codigo_dot)
        archivo.close()

        # Generamos la imagen
        comando = f'dot -Tpng {ruta_dot} -o {ruta_imagen}'
        os.system(comando)

        # Abrimos la imagen
        os.startfile(os.path.abspath(ruta_imagen))