class Nodo:
    def __init__(self, nombre_producto, precio_producto, cantidad_producto):
        self.nombre_producto = nombre_producto
        self.precio_producto = precio_producto
        self.cantidad_producto = cantidad_producto
        self.abajo = None
