class Nodo:
    def __init__(self, usuario_id, nombre_usuario, productos, total):
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.productos = productos
        self.total = total
        self.siguiente = None
