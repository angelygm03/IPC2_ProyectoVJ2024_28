# lista_dobleCircular/lista_dobleCircular.py
from .nodo import NodoProducto

class ListaDobleCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, producto):
        nuevo_nodo = NodoProducto(producto)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.primero.siguiente = self.primero
            self.primero.anterior = self.ultimo
        else:
            nuevo_nodo.anterior = self.ultimo
            nuevo_nodo.siguiente = self.primero
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.primero.anterior = self.ultimo

    def imprimir(self):
        if self.esta_vacia():
            print("La lista está vacía")
            return
        actual = self.primero
        while True:
            producto = actual.producto
            print(f"\n ID: {producto.id}, \n Nombre: {producto.nombre} \n Precio: {producto.precio} \n Descripción: {producto.descripcion} \n Categoría: {producto.categoria} \n Cantidad: {producto.cantidad} \n Imagen: {producto.imagen}")
            actual = actual.siguiente
            if actual == self.primero:
                break
