from .nodo import NodoEmpleado

class ListaCircularSimple:
    def __init__(self):
        self.primero = None

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, empleado):
        nuevo_nodo = NodoEmpleado(empleado)
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo  # El primer nodo apunta a sí mismo
            self.primero = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero.siguiente
            self.primero.siguiente = nuevo_nodo

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