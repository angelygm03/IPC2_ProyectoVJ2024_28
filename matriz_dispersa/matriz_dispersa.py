from .listaCabecera import ListaCabecera
from .nodoCabecera import NodoCabecera
from .nodoCelda import NodoCelda
import os

class MatrizDispersa:
    def __init__(self):
        self.filas = ListaCabecera("fila")
        self.columnas = ListaCabecera("columna")
    
    #Insertar celdas y columnas
    def insertar(self, x, y, empleado):
        nuevo = NodoCelda(x, y, empleado) #se crea el nodo de la celda

        # Para ver si ya existe la cabecera de las celdas y columnas en la matriz
        celda_x = self.filas.obtenerCabecera(x)
        celda_y = self.columnas.obtenerCabecera(y)

        #Se verifica si la cabecera de la fila X existe
        if celda_x == None:
            #Si no existe entonces se crea una nueva cabecera de la fila
            celda_x = NodoCabecera(x)
            self.filas.insertarNodoCabecera(celda_x)

        #Se verifica si la cabecera de la columna Y existe
        if celda_y == None:
            #Si no existe entonces se crea una nueva cabecera columna
            celda_y = NodoCabecera(y)
            self.columnas.insertarNodoCabecera(celda_y)

        #Insertar celda en la fila
        if celda_x.acceso == None:
            celda_x.acceso = nuevo
        else:
            if nuevo.y < celda_x.acceso.y:
                nuevo.derecha = celda_x.acceso
                celda_x.acceso.izquierda = nuevo
                celda_x.acceso = nuevo
            else:
                #Recorrer la fila de izquierda a derecha
                actual = celda_x.acceso
                while actual != None:
                    #Si la columna del nuevo nodo es menor a la columna del nodo actual
                    if nuevo.y < actual.y:
                        nuevo.derecha = actual
                        nuevo.izquierda = actual.izquierda
                        actual.izquierda.derecha = nuevo
                        actual.izquierda = nuevo
                        break
                    elif nuevo.x == actual.x and nuevo.y == actual.y:
                        break
                    else:
                        if actual.derecha == None:
                            actual.derecha = nuevo
                            nuevo.izquierda = actual
                            break
                        else:
                            actual = actual.derecha

        #Insertar celda en la columna
        if celda_y.acceso == None:
            celda_y.acceso = nuevo
        else:
            if nuevo.x < celda_y.acceso.x:
                nuevo.abajo = celda_y.acceso
                celda_y.acceso.arriba = nuevo
                celda_y.acceso = nuevo
            #Se inserta el nodo en la columna de arriba hacia abajo
            else:
                actual2 = celda_y.acceso
                while actual2 != None:
                    if nuevo.x < actual2.x:
                        nuevo.abajo = actual2
                        nuevo.arriba = actual2.arriba
                        actual2.arriba.abajo = nuevo
                        actual2.arriba = nuevo
                        break
                    elif nuevo.x == actual2.x and nuevo.y == actual2.y:
                        break
                    else:
                        if actual2.abajo == None:
                            actual2.abajo = nuevo
                            nuevo.arriba = actual2
                            break
                        else:
                            actual2 = actual2.abajo
    
    def recorridoFilas(self, fila):
        inicio = self.filas.obtenerCabecera(fila)
        if inicio == None:
            print('La fila no existe')
            return 

        actual = inicio.acceso
        while actual != None:
            print(f'{str(actual.x)}, {str(actual.y)} = {str(actual.empleado)}')
            actual = actual.derecha

    def recorridoColumnas(self, columna):
        inicio = self.columnas.obtenerCabecera(columna)
        if inicio == None:
            print('La columna no existe')
            return 
        
        actual = inicio.acceso
        while actual != None:
            print(f'{str(actual.x)}, {str(actual.y)} = {str(actual.empleado)}')
            actual = actual.abajo
    
    #función para imprimir la matriz con los atributos en consola
    def imprimir(self):
        #Se recorre la matriz de arriba hacia abajo
        actual = self.filas.primero
        while actual != None:
            aux = actual.acceso
            while aux != None:
                print(f'{str(aux.x)}, {str(aux.y)} = {str(aux.empleado)}')
                aux = aux.derecha
            actual = actual.siguiente
    
    #función para graficar la matriz en un archivo .png
    def graficar(self):
        codigodot = ''
        ruta_directorio_dot = './reportedot'
        ruta_directorio_img = './Reportes'
        ruta_dot = f'{ruta_directorio_dot}/ListaOrtogonal.dot'
        ruta_png = f'{ruta_directorio_img}/ListaOrtogonal.png'

        # Crear los directorios si no existen
        if not os.path.exists(ruta_directorio_dot):
            os.makedirs(ruta_directorio_dot)
        if not os.path.exists(ruta_directorio_img):
            os.makedirs(ruta_directorio_img)

        codigodot += '''digraph G {
    graph [pad=\"0.5\", nodesep=\"1\", ranksep=\"1\"];
    label=\"Calendario de Actividades\"
    node [shape=box, height=0.8];\n'''
        
        #1. GRAFICAMOS DESDE LAS FILAS
        filaActual = self.filas.primero
        idFila = ''
        conexionesFilas = ''
        nodosInteriores = ''
        direccionInteriores = ''
        while(filaActual != None):
            primero = True
            actual = filaActual.acceso
            #GRAFICA LA CABECERA DE LA FILA
            idFila += '\tFila'+str(actual.x)+'[style=\"filled\" label = \"'+str(filaActual.id)+'\" fillcolor="white" group = 0];\n'
            #ENLAZA LA CABECERA DE LA FILA CON EL PRIMER NODO DE LA FILA (OSEA EL ACCESO)
            if filaActual.siguiente != None:
                conexionesFilas += '\tFila'+str(actual.x)+' -> Fila'+str(filaActual.siguiente.acceso.x)+';\n'
            direccionInteriores += '\t{ rank = same; Fila'+str(actual.x)+'; '
            while actual != None:
                nodosInteriores += '\tNodoF'+str(actual.x)+"_C"+str(actual.y)+'[style=\"filled\" label = \"'+str(actual.empleado)+'\" group = '+str(actual.y)+'];\n'
                direccionInteriores += 'NodoF'+str(actual.x)+"_C"+str(actual.y)+'; '
                #ES PARA QUE APUNTE LA CABECERA DE LA FILA AL PRIMER NODO DE LA FILA
                if primero == True:
                    nodosInteriores += '\tFila'+str(actual.x)+' -> NodoF'+str(actual.x)+"_C"+str(actual.y)+'[dir=""];\n'
                    if actual.derecha != None:
                        nodosInteriores += '\tNodoF'+str(actual.x)+"_C"+str(actual.y)+' -> NodoF'+str(actual.derecha.x)+"_C"+str(actual.derecha.y)+';\n'
                    primero = False
                else:
                    if actual.derecha != None:
                        nodosInteriores += '\tNodoF'+str(actual.x)+"_C"+str(actual.y)+' -> NodoF'+str(actual.derecha.x)+"_C"+str(actual.derecha.y)+';\n'
                actual = actual.derecha
            filaActual = filaActual.siguiente
            direccionInteriores += '}\n'

        codigodot += idFila + '''
    edge[dir="both"];
    '''+conexionesFilas+'''
    edge[dir="both"]
    '''
        
        #2. GRAFICAR COLUMNAS
        columnaActual = self.columnas.primero
        idColumna = ''
        conexionesColumnas = ''
        direccionInteriores2 = '\t{rank = same; '
        while columnaActual != None:
            primero = True
            actual = columnaActual.acceso
            idColumna += '\tColumna'+str(actual.y)+'[style=\"filled\" label = \"'+str(actual.y)+'\" fillcolor="white" group = '+str(actual.y)+'];\n'
            direccionInteriores2 += 'Columna'+str(actual.y)+'; '
            if(columnaActual.siguiente != None):
                conexionesColumnas += 'Columna'+str(actual.y)+' -> Columna'+str(columnaActual.siguiente.acceso.y)+';\n'
            while actual != None:
                if primero == True:
                    codigodot += 'Columna'+str(actual.y)+' -> NodoF'+str(actual.x)+"_C"+str(actual.y)+'[dir=""];\n'
                    if actual.abajo != None:
                        codigodot += 'NodoF'+str(actual.x)+"_C"+str(actual.y)+' -> NodoF'+str(actual.abajo.x)+"_C"+str(actual.abajo.y)+';\n'
                    primero = False
                else:
                    if actual.abajo != None:
                        codigodot += 'NodoF'+str(actual.x)+"_C"+str(actual.y)+' -> NodoF'+str(actual.abajo.x)+"_C"+str(actual.abajo.y)+';\n'
                actual = actual.abajo
            columnaActual = columnaActual.siguiente
        codigodot += idColumna 
        codigodot += conexionesColumnas + '\n'
        codigodot += direccionInteriores2 + '}\n'
        codigodot += nodosInteriores
        codigodot += direccionInteriores
        codigodot += '\n}'

        with open(ruta_dot, 'w') as archivo:
            archivo.write(codigodot)

        #Generamos la imagen
        ruta_dot = 'reportedot/ListaOrtogonal.dot'
        ruta_png = 'Reportes/ListaOrtogonal.png'

        comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_png
        os.system(comando)

        #Abrimos el archivo
        ruta = os.path.abspath(ruta_png)
        os.startfile(ruta)




    