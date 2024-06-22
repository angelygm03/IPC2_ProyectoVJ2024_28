from clases.usuario import Usuario
from clases.producto import Producto
from clases.empleado import Empleado

class Manager():
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.empleados = []
    
    def addUsuario(self, id, nombre, edad, email, telefono, password):
        usuario = Usuario(id, nombre, edad, email, telefono, password)
        self.usuarios.append(usuario)
        return True
    
    def getUsuario(self):
        json = []
        for i in self.usuarios:
            usuario = {
                'id': i.id,
                'nombre': i.nombre,
                'edad': i.edad,
                'email': i.email,
                'telefono': i.telefono,
                'password': i.password
            }
            json.append(usuario)
        return json

    def addProducto(self, id, nombre, precio, descripcion, categoria, cantidad, imagen):
        producto = Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
        self.productos.append(producto)
        return True
    
    def getProducto(self):
        json = []
        for p in self.productos:
            producto = {
                'id': p.id,
                'nombre': p.nombre,
                'precio': p.precio,
                'descripcion': p.descripcion,
                'categoria': p.categoria,
                'cantidad': p.cantidad,
                'imagen': p.imagen
            }
            json.append(producto)
        return json
    
    def addEmpleado(self, codigo, nombre, puesto):
        empleado = Empleado(codigo, nombre, puesto)
        self.empleados.append(empleado)
        return True
    
    def getEmpleado(self):
        json = []
        for e in self.empleados:
            empleado = {
                'codigo': e.codigo,
                'nombre': e.nombre,
                'puesto': e.puesto
            }
            json.append(empleado)
        return json

    def agregarCarrito(self, user_id, product_id):
        usuario = next((u for u in self.usuarios if u.id == user_id), None)
        producto = next((p for p in self.productos if p.id == product_id), None)
        if usuario and producto:
            usuario.agregarCarrito(producto)
            return True
        return False

    def getCarrito(self, user_id):
        usuario = next((u for u in self.usuarios if u.id == user_id), None)
        if usuario:
            return usuario.get_carrito()
        return []

    def empty_carrito(self, user_id):
        usuario = next((u for u in self.usuarios if u.id == user_id), None)
        if usuario:
            usuario.empty_carrito()
            return True
        return False