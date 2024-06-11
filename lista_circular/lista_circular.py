from .nodo import NodoEmpleado

class ListaCircularSimple:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, empleado):
        nuevo_nodo = NodoEmpleado(empleado)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.ultimo.siguiente = self.primero
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.ultimo.siguiente = self.primero
        self.tamanio += 1

    def imprimir(self):
        if self.esta_vacia():
            print("La lista de empleados está vacía")
            return
        actual = self.primero
        while True:
            print("Código:", actual.empleado.codigo)
            print("Nombre:", actual.empleado.nombre)
            print("Puesto:", actual.empleado.puesto)
            print()
            actual = actual.siguiente
            if actual == self.primero:
                break
