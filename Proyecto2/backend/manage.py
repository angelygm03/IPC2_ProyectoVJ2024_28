from clases.usuario import Usuario
from clases.producto import Producto
from clases.empleado import Empleado
from clases.actividad import Actividad
import xml.etree.ElementTree as ET
import os

class Manager():
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.empleados = []
        self.carritos = {}
        self.compras = {}
        self.actividades = []
        self.database_path = os.path.join(os.path.dirname(__file__), 'database')
        os.makedirs(self.database_path, exist_ok=True)
        self.load_data()

    def load_data(self):
        self.load_usuarios()
        self.load_productos()
        self.load_empleados()
        self.load_carritos()
        self.load_compras()
        self.load_actividades()

    def save_data(self):
        self.save_usuarios()
        self.save_productos()
        self.save_empleados()
        self.save_carritos()
        self.save_compras()
        self.save_actividades()

    def load_usuarios(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'usuarios.xml'))
            root = tree.getroot()
            for elemento in root:
                id = elemento.attrib.get('id')
                nombre = elemento.find('nombre').text
                edad = int(elemento.find('edad').text)
                email = elemento.find('email').text
                telefono = elemento.find('telefono').text
                password = elemento.find('password').text
                self.usuarios.append(Usuario(id, nombre, edad, email, telefono, password))
        except FileNotFoundError:
            pass

    def save_usuarios(self):
        root = ET.Element("usuarios")
        for usuario in self.usuarios:
            usuario_elem = ET.SubElement(root, "usuario", id=usuario.id)
            ET.SubElement(usuario_elem, "nombre").text = usuario.nombre
            ET.SubElement(usuario_elem, "edad").text = str(usuario.edad)
            ET.SubElement(usuario_elem, "email").text = usuario.email
            ET.SubElement(usuario_elem, "telefono").text = usuario.telefono
            ET.SubElement(usuario_elem, "password").text = usuario.password
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.database_path, 'usuarios.xml'), encoding='utf-8', xml_declaration=True)

    def load_productos(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'productos.xml'))
            root = tree.getroot()
            for elemento in root:
                id = elemento.attrib.get('id')
                nombre = elemento.find('nombre').text
                precio = float(elemento.find('precio').text)
                descripcion = elemento.find('descripcion').text
                categoria = elemento.find('categoria').text
                cantidad = int(elemento.find('cantidad').text)
                imagen = elemento.find('imagen').text
                self.productos.append(Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen))
        except FileNotFoundError:
            pass

    def save_productos(self):
        root = ET.Element("productos")
        for producto in self.productos:
            producto_elem = ET.SubElement(root, "producto", id=producto.id)
            ET.SubElement(producto_elem, "nombre").text = producto.nombre
            ET.SubElement(producto_elem, "precio").text = str(producto.precio)
            ET.SubElement(producto_elem, "descripcion").text = producto.descripcion
            ET.SubElement(producto_elem, "categoria").text = producto.categoria
            ET.SubElement(producto_elem, "cantidad").text = str(producto.cantidad)
            ET.SubElement(producto_elem, "imagen").text = producto.imagen
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.database_path, 'productos.xml'), encoding='utf-8', xml_declaration=True)

    def load_empleados(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'empleados.xml'))
            root = tree.getroot()
            for elemento in root:
                codigo = elemento.attrib.get('codigo')
                nombre = elemento.find('nombre').text
                puesto = elemento.find('puesto').text
                self.empleados.append(Empleado(codigo, nombre, puesto))
        except FileNotFoundError:
            pass

    def save_empleados(self):
        root = ET.Element("empleados")
        for empleado in self.empleados:
            empleado_elem = ET.SubElement(root, "empleado", codigo=empleado.codigo)
            ET.SubElement(empleado_elem, "nombre").text = empleado.nombre
            ET.SubElement(empleado_elem, "puesto").text = empleado.puesto
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.database_path, 'empleados.xml'), encoding='utf-8', xml_declaration=True)

    def load_carritos(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'carritos.xml'))
            root = tree.getroot()
            for elemento in root:
                user_id = elemento.attrib.get('user_id')
                self.carritos[user_id] = []
                for prod_elem in elemento.findall('producto'):
                    product_id = prod_elem.attrib.get('id')
                    cantidad = int(prod_elem.find('cantidad').text)
                    self.carritos[user_id].extend([product_id] * cantidad)
        except FileNotFoundError:
            pass

    def save_carritos(self):
        root = ET.Element("carritos")
        for user_id, productos in self.carritos.items():
            carrito_elem = ET.SubElement(root, "carrito", user_id=user_id)
            producto_cantidades = {}
            for product_id in productos:
                if product_id in producto_cantidades:
                    producto_cantidades[product_id] += 1
                else:
                    producto_cantidades[product_id] = 1
            for product_id, cantidad in producto_cantidades.items():
                producto_elem = ET.SubElement(carrito_elem, "producto", id=product_id)
                ET.SubElement(producto_elem, "cantidad").text = str(cantidad)
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.database_path, 'carritos.xml'), encoding='utf-8', xml_declaration=True)

    def load_compras(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'compras.xml'))
            root = tree.getroot()
            for elemento in root:
                user_id = elemento.attrib.get('user_id')
                self.compras[user_id] = []
                for prod_elem in elemento.findall('producto'):
                    product_id = prod_elem.attrib.get('id')
                    cantidad = int(prod_elem.find('cantidad').text)
                    self.compras[user_id].extend([product_id] * cantidad)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    def save_compras(self):
        try:
            root = ET.Element("compras")
            for user_id, productos in self.compras.items():
                compra_elem = ET.SubElement(root, "compra", user_id=user_id)
                producto_cantidades = {}
                for product_id in productos:
                    if product_id in producto_cantidades:
                        producto_cantidades[product_id] += 1
                    else:
                        producto_cantidades[product_id] = 1
                for product_id, cantidad in producto_cantidades.items():
                    producto_elem = ET.SubElement(compra_elem, "producto", id=product_id)
                    ET.SubElement(producto_elem, "cantidad").text = str(cantidad)
            self.indent_xml(root)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(self.database_path, 'compras.xml'), encoding='utf-8', xml_declaration=True)
            print("Compras guardadas correctamente en 'compras.xml'")
        except Exception as e:
            print(f"Error al guardar 'compras.xml': {e}")

    def load_actividades(self):
        try:
            tree = ET.parse(os.path.join(self.database_path, 'actividades.xml'))
            root = tree.getroot()
            for elemento in root:
                id = elemento.attrib.get('id')
                nombre = elemento.find('nombre').text
                descripcion = elemento.find('descripcion').text
                empleado = elemento.find('empleado').text
                dia = int(elemento.find('dia').text)
                hora = int(elemento.find('hora').text)
                self.actividades.append(Actividad(id, nombre, descripcion, empleado, dia, hora))
        except FileNotFoundError:
            pass

    def save_actividades(self):
        root = ET.Element("actividades")
        for actividad in self.actividades:
            actividad_elem = ET.SubElement(root, "actividad", id=actividad.id)
            ET.SubElement(actividad_elem, "nombre").text = actividad.nombre
            ET.SubElement(actividad_elem, "descripcion").text = actividad.descripcion
            ET.SubElement(actividad_elem, "empleado").text = actividad.empleado
            ET.SubElement(actividad_elem, "dia").text = str(actividad.dia)
            ET.SubElement(actividad_elem, "hora").text = str(actividad.hora)
        self.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.database_path, 'actividades.xml'), encoding='utf-8', xml_declaration=True)


    def addUsuario(self, id, nombre, edad, email, telefono, password):
        usuario = Usuario(id, nombre, edad, email, telefono, password)
        self.usuarios.append(usuario)
        self.save_usuarios()
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
        self.save_productos()
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
        self.save_empleados()
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

    def agregarCarrito(self, user_id, product_id, cantidad):
        if user_id not in self.carritos:
            self.carritos[user_id] = [] 
        for _ in range(cantidad): 
            self.carritos[user_id].append(product_id)
            self.save_carritos()
        return True

    def obtenerCarrito(self, user_id):
        carrito = self.carritos.get(user_id, [])
        print(f"Obteniendo carrito para {user_id}: {carrito}")
        return carrito

    def obtenerListaCompras(self, user_id):
        compras = self.compras.get(user_id, [])
        print(f"Obteniendo lista de compras para {user_id}: {compras}")
        self.save_compras()
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
    
    def addActividad(self, id, nombre, descripcion, empleado, dia, hora):
        actividad = Actividad(id, nombre, descripcion, empleado, dia, hora)
        self.actividades.append(actividad)
        self.save_actividades()
        return True

    def getActividades(self):
        return [actividad.to_dict() for actividad in self.actividades]
    

    def obtenerNombreEmpleado(self, empleado_id):
        for empleado in self.empleados:
            if empleado.codigo == empleado_id:
                return empleado.nombre
        return "Nombre del Empleado"
