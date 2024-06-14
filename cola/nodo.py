class Nodo:
    def __init__(self, id_usuario, nombre_usuario, productos, total):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.productos = productos
        self.total = total
        self.siguiente = None
