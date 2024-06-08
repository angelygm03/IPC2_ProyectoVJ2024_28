# lista_doble/lista_doble.py
from .nodo import Nodo

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
