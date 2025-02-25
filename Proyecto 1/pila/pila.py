import os
from pila.nodo import Nodo

class Pila:
    def __init__(self):
        self.cima = None
        self.tamanio = 0

    def push(self, nombre_producto, precio_producto, cantidad_producto):
        nuevo_nodo = Nodo(nombre_producto, precio_producto, cantidad_producto)
        nuevo_nodo.abajo = self.cima
        self.cima = nuevo_nodo
        self.tamanio += 1

    def pop(self):
        if self.cima is None:
            print('Pila vacía')
            return None
        nodo_a_eliminar = self.cima
        self.cima = self.cima.abajo
        self.tamanio -= 1
        return nodo_a_eliminar

    def peek(self):
        if self.cima is None:
            print('Pila vacía')
            return None
        return self.cima

    def isEmpty(self):
        return self.cima is None
    
    def __len__(self):
        return self.tamanio

    def mostrar(self):
        if self.cima is None:
            print('Pila vacía')
            return
        actual = self.cima
        print("Productos en el carrito:")
        while actual is not None:
            print(f"Producto: {actual.nombre_producto}, Precio: {actual.precio_producto}, Cantidad: {actual.cantidad_producto}")
            actual = actual.abajo

    def graficar(self, usuario_id):
        if self.isEmpty():
            print('Pila vacía')
            return
        codigodot = ''
        ruta_directorio_dot = './reportedot'
        ruta_directorio_img = './Reportes'
        ruta_dot = f'{ruta_directorio_dot}/Pila{usuario_id}.dot'
        ruta_imagen = f'{ruta_directorio_img}/Pila{usuario_id}.png'

        if not os.path.exists(ruta_directorio_dot):
            os.makedirs(ruta_directorio_dot)
        if not os.path.exists(ruta_directorio_img):
            os.makedirs(ruta_directorio_img)

        archivo = open(ruta_dot, 'w')
        codigodot += '''digraph G {
    rankdir=LR;
    node[shape=Mrecord];\n'''
        nodos = 'Nodo[xlabel = Carrito label = "'
        actual = self.cima
        while actual is not None:
            if actual.abajo is not None:
                nodos += f"Producto: {actual.nombre_producto}, Precio: {actual.precio_producto}, Cantidad: {actual.cantidad_producto} |"
            else:
                nodos += f"Producto: {actual.nombre_producto}, Precio: {actual.precio_producto}, Cantidad: {actual.cantidad_producto}"
            actual = actual.abajo
        nodos += '"];\n'
        codigodot += nodos + "}"

        archivo.write(codigodot)
        archivo.close()

        comando = 'dot -Tpng ' + ruta_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_salida2 = os.path.abspath(ruta_imagen)
        os.startfile(ruta_salida2)
