class Usuario:
    def __init__(self, id, nombre, edad, email, telefono, password):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.telefono = telefono
        self.password = password
        self.carrito = []  # Inicializamos el carrito como una lista vacía

    def agregarCarrito(self, producto):
        self.carrito.append(producto)

    def getCarrito(self):
        return self.carrito

    def empty_carrito(self):
        self.carrito = []
    
    def getUsuario(self):
        return self
    