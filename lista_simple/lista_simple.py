from lista_simple.nodo import Nodo
import os

class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def insertar(self, usuario_id, nombre_usuario, productos, total):
        nuevo = Nodo(usuario_id, nombre_usuario, productos, total)
        if self.cabeza == None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente != None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1


    def mostrar(self):
        if self.cabeza is None:
            print("No hay solicitudes aceptadas.")
            return
        actual = self.cabeza
        while actual is not None:
            print(f"Solicitud aceptada: Usuario ID: {actual.usuario_id}, Nombre: {actual.nombre_usuario}, Productos: {actual.productos}, Total: {actual.total}")
            actual = actual.siguiente

    def graficar(self):
        codigodot = ''
        ruta_directorio_dot = './reportedot'
        ruta_directorio_img = './Reportes'
        ruta_dot = f'{ruta_directorio_dot}/ListaCompras.dot'
        ruta_imagen = f'{ruta_directorio_img}/ListaCompras.png'

        # Crear los directorios si no existen
        if not os.path.exists(ruta_directorio_dot):
            os.makedirs(ruta_directorio_dot)
        if not os.path.exists(ruta_directorio_img):
            os.makedirs(ruta_directorio_img)

        archivo = open(ruta_dot, 'w')
        codigodot += '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]'''
        contador_nodos = 0
        #PRIMERO CREAMOS LOS NODOS
        actual = self.cabeza
        while actual is not None:
            etiqueta = f"ID: {actual.usuario_id}\\nNombre: {actual.nombre_usuario}\\nProductos: {actual.productos}\\nTotal: {actual.total}"
            codigodot += f'node{contador_nodos} [label = \"{{ {etiqueta} |<f1> }}\"];\n'
            contador_nodos += 1
            actual = actual.siguiente

        #AHORA CREAMOS LAS RELACIONES
        actual = self.cabeza
        contador_nodos = 0
        while actual.siguiente != None:
            codigodot += f'node{contador_nodos}->node{contador_nodos + 1};\n'
            contador_nodos += 1
            actual = actual.siguiente

        codigodot += '}'

        #Lo escribimos en el archivo dot
        archivo.write(codigodot)
        archivo.close()

        #Generamos la imagen
        comando = f'dot -Tpng {ruta_dot} -o {ruta_imagen}'
        os.system(comando)
        #Abrir la imagen
        ruta_abrir_reporte = os.path.abspath(ruta_imagen)
        os.startfile(ruta_abrir_reporte)