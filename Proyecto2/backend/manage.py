from clases.usuario import Usuario
from clases.producto import Producto
from clases.empleado import Empleado
import xml.etree.ElementTree as ET

class Manager():
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.empleados = []
        self.carritos = {}
        self.compras = {}

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

    def agregarCarrito(self, user_id, product_ids):
        if user_id not in self.carritos:
            self.carritos[user_id] = []  # Inicializa el carrito si no existe
        if not isinstance(product_ids, list):
            product_ids = [product_ids]
        self.carritos[user_id].extend(product_ids)
        return True

    def obtenerCarrito(self, user_id):
        carrito = self.carritos.get(user_id, [])
        print(f"Obteniendo carrito para {user_id}: {carrito}")
        return carrito

    def obtenerListaCompras(self, user_id):
        compras = self.compras.get(user_id, [])
        print(f"Obteniendo lista de compras para {user_id}: {compras}")
        return compras

    def obtenerNombreProducto(self, product_id):
        for producto in self.productos:
            if producto.id == product_id:
                return producto.nombre  
        return "Nombre del Producto"
    
    def obtenerPrecioProducto(self, product_id):
        for producto in self.productos:
            if producto.id == product_id:
                return producto.precio  
        return 0

    def obtenerNombreUsuario(self, user_id):
        for usuario in self.usuarios:
            if usuario.id == user_id:
                return usuario.nombre
        return "Nombre del Usuario"

    def generarXMLCarrito(self, user_id):
        carrito = self.obtenerCarrito(user_id)
        producto_cantidades = {}

        for product_id in carrito:
            if product_id in producto_cantidades:
                producto_cantidades[product_id] += 1
            else:
                producto_cantidades[product_id] = 1

        root = ET.Element("carrito")

        for product_id, cantidad in producto_cantidades.items():
            product_name = self.obtenerNombreProducto(product_id)
            producto_elem = ET.SubElement(root, "producto", id=product_id)
            ET.SubElement(producto_elem, "nombre").text = product_name
            ET.SubElement(producto_elem, "cantidad").text = str(cantidad)

        self.indent_xml(root)
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        full_xml_str = xml_declaration + xml_str

        return full_xml_str


    def indent_xml(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i