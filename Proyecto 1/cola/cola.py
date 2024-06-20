from cola.nodo import Nodo
import os
import tkinter as tk

class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def enqueue(self, id_usuario, nombre_usuario, productos, total):
        nuevo = Nodo(id_usuario, nombre_usuario, productos, total)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.tamanio += 1

    def dequeue(self):
        if self.primero is None:
            print('Cola vacía')
            return None
        else:
            nodo_a_eliminar = self.primero
            self.primero = self.primero.siguiente
            if self.primero is None:
                self.ultimo = None
            self.tamanio -= 1
            return nodo_a_eliminar

    def verPrimero(self):
        if self.primero is None:
            print('Cola vacía')
            return None
        return self.primero
    
    def __len__(self):
        return self.tamanio

    def mostrar(self):
        if self.primero is None:
            print('Cola vacía')
            return
        actual = self.primero
        while actual is not None:
            print(f"Solicitud de compra, Usuario: {actual.id_usuario}, Nombre: {actual.nombre_usuario}, Productos: {actual.productos}, Total: {actual.total}")
            actual = actual.siguiente

    def isEmpty(self):
        return self.primero is None

    def mostrar_en_text_area(self, text_area):
        text_area.delete(1.0, tk.END)
        if self.primero is None:
            text_area.insert(tk.END, "No hay solicitudes pendientes.")
            return
        actual = self.primero
        while actual is not None:
            text_area.insert(tk.END, f"ID Usuario: {actual.id_usuario}\n")
            text_area.insert(tk.END, f"Nombre Usuario: {actual.nombre_usuario}\n")
            text_area.insert(tk.END, f"Productos:\n{actual.productos}\n")
            text_area.insert(tk.END, f"Total: {actual.total}\n")
            text_area.insert(tk.END, "\n---------------------------------------------------\n")
            actual = actual.siguiente
    
    def graficar(self):
        codigodot = ''
        ruta_directorio_dot = './reportedot'
        ruta_directorio_img = './Reportes'
        ruta_dot = f'{ruta_directorio_dot}/ColaSolicitudesCompra.dot'
        ruta_imagen = f'{ruta_directorio_img}/ColaSolicitudesCompra.png'

        if not os.path.exists(ruta_directorio_dot):
            os.makedirs(ruta_directorio_dot)
        if not os.path.exists(ruta_directorio_img):
            os.makedirs(ruta_directorio_img)

        archivo = open(ruta_dot, 'w')
        codigodot += '''digraph G {
    rankdir="RL";
    label="Solicitudes de Compra";
    node[shape=box];'''

        contador = 0
        actual = self.primero
        conexiones = ''
        nodos = ''
        while actual != None:
            nodos += f'Nodo{contador}[label="ID: {actual.id_usuario}\\nNombre: {actual.nombre_usuario}\\nProductos: {actual.productos}\\nTotal: Q{actual.total}"];\n'
            if actual.siguiente != None:
                conexiones += f'Nodo{contador+1} -> Nodo{contador};\n'
            contador += 1
            actual = actual.siguiente
        
        codigodot += nodos + "\n" + conexiones + '\n}'

        archivo.write(codigodot)
        archivo.close()

        comando = f'dot -Tpng {ruta_dot} -o {ruta_imagen}'
        os.system(comando)

        ruta_salida2 = os.path.abspath(ruta_imagen)
        os.startfile(ruta_salida2)