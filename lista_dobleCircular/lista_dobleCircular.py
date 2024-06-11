# lista_dobleCircular/lista_dobleCircular.py
from .nodo import NodoProducto

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
            print(f"\n ID: {producto.id}, \n Nombre: {producto.nombre} \n Precio: {producto.precio} \n Descripción: {producto.descripcion} \n Categoría: {producto.categoria} \n Cantidad: {producto.cantidad} \n Imagen: {producto.imagen}")
            actual = actual.siguiente
            if actual == self.primero:
                break

                


    


