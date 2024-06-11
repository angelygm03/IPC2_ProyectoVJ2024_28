from .nodo import NodoEmpleado
import os

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
    
    def graficar(self):
        # Crear los directorios si no existen
        os.makedirs('reportedot', exist_ok=True)
        os.makedirs('Reportes', exist_ok=True)
        
        # Abrir el archivo en modo escritura con codificación UTF-8
        with open('reportedot/ListaVendedores.dot', 'w', encoding='utf-8') as archivo:
            codigo_dot = '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]\n'''
            
            # Crear los nodos con los detalles de los empleados y un campo vacío adicional
            contador_nodos = 0
            actual = self.primero
            while contador_nodos < self.tamanio:
                empleado = actual.empleado
                codigo_dot += f'node{contador_nodos} [label = "{{Código: {empleado.codigo} \\nNombre: {empleado.nombre}\\nPuesto: {empleado.puesto}|<f1>}}"];\n'
                actual = actual.siguiente
                contador_nodos += 1

            # Crear las relaciones o apuntadores
            contador_nodos = 0
            actual = self.primero
            while contador_nodos < self.tamanio - 1:
                codigo_dot += f'node{contador_nodos} -> node{contador_nodos + 1};\n'
                actual = actual.siguiente
                contador_nodos += 1
            
            # Agregar la relación del nodo final con el nodo inicial
            codigo_dot += f'node{self.tamanio - 1} -> node0 [constraint=false];\n'

            codigo_dot += '}'

            # Escribir el contenido DOT en el archivo
            archivo.write(codigo_dot)

        # Generar la imagen
        ruta_dot = 'reportedot/ListaVendedores.dot'
        ruta_imagen = 'Reportes/ListaVendedores.png'
        comando = f'dot -Tpng {ruta_dot} -o {ruta_imagen}'
        os.system(comando)

        # Abrir la imagen
        ruta_reporte2 = os.path.abspath(ruta_imagen)
        os.startfile(ruta_reporte2)