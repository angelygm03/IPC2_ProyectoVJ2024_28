class Usuario:
    def __init__(self, id, nombre, edad, email, telefono, password):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.telefono = telefono
        self.password = password
        self.carrito = []

    def agregarCarrito(self, producto):
        self.carrito.append(producto)

    def get_carrito(self):
        return [p.__dict__ for p in self.carrito]

    def empty_carrito(self):
        self.carrito = []
