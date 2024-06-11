# lista_dobleCircular/lista_dobleCircular.py
from .nodo import NodoProducto
import os

class ListaDobleCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def esta_vacia(self):
        return self.primero is None
    
    def agregar(self, producto):
        nuevo = NodoProducto(producto)
        # Si esta vacia la lista
        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        # Si la lista tiene mínimo 1 elemento
        else:
            # 1. El siguiente del ultimo nodo es el nuevo nodo
            self.ultimo.siguiente = nuevo
            # 2. El anterior del nuevo nodo es el ultimo nodo
            nuevo.anterior = self.ultimo
            # 3. El ultimo nodo es el nuevo nodo
            self.ultimo = nuevo
            # 4. El siguiente del ultimo nodo es el primer nodo
            self.ultimo.siguiente = self.primero
            # 5. El anterior del primer nodo es el ultimo nodo
            self.primero.anterior = self.ultimo
        self.tamanio += 1

    def imprimir(self):
        if self.esta_vacia():
            print("La lista está vacía")
            return
        actual = self.primero
        while True:
            producto = actual.producto
            print(f"\n ID: {producto.id}, \n Nombre: {producto.nombre} \n Precio: {producto.precio} \n Descripción: {producto.descripcion} \n Categoría: {producto.categoria} \n Cantidad: {producto.cantidad}")
            actual = actual.siguiente
            if actual == self.primero:
                break

    def graficar(self):
        codigodot = ''
        
        os.makedirs('reportedot', exist_ok=True)
        
        archivo = open('reportedot/ListaProductos.dot', 'w')
        codigodot += '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]\n'''
        
        actual = self.primero
        contador = 0
        while contador < self.tamanio:
            producto = actual.producto
            # Construir la etiqueta del nodo con los atributos del producto
            etiqueta = f"ID: {producto.id} \\n Nombre: {producto.nombre} \\n Precio: {producto.precio} \\n Descripción: {producto.descripcion} \\n Categoría: {producto.categoria} \\n Cantidad: {producto.cantidad}"
            codigodot += f'node{contador} [label = "{{<f1>|{etiqueta}|<f2>}}"];\n'
            actual = actual.siguiente
            contador += 1

        contador = 0
        actual = self.primero
        while contador < self.tamanio - 1:
            codigodot += f'node{contador}:f2 -> node{contador + 1}:f1 [dir=both];\n'
            contador += 1
            actual = actual.siguiente

        codigodot += f'node0:f1 -> node{self.tamanio - 1}:f2 [dir=both constraint=false];\n'

        codigodot += '}'

        archivo.write(codigodot)
        archivo.close()

        os.makedirs('Reportes', exist_ok=True)
        ruta_dot = 'reportedot/ListaProductos.dot'
        ruta_png = 'Reportes/ListaProductos.png'
        comando = f'dot -Tpng {ruta_dot} -o {ruta_png}'
        os.system(comando)

        ruta_salida = os.path.abspath(ruta_png)
        os.startfile(ruta_salida)