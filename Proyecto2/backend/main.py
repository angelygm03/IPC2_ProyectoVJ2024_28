from flask import Flask, request, jsonify, Response
from flask.json import jsonify
from xml.etree import ElementTree as ET
from manage import Manager
from flask_cors import CORS

app = Flask(__name__)
manager = Manager()
cors = CORS(app)


@app.route('/')
def index():
    return "API con Python y Flask funcionando correctamente"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    id = data.get('id')
    password = data.get('password')
    if id == 'AdminIPC2' and password == 'IPC2VJ2024':
        return jsonify({
                        'message': 'Usuario logueado correctamente',
                        'role': 1,
                        'status': 200
                    })
    else:
        for i in manager.usuarios:
            if i.id == id and i.password == password:
                return jsonify({
                        'message': 'Usuario logueado correctamente',
                        'role': 2,
                        'status': 200
                    })
        return jsonify({"message": "Credenciales incorrectas"}), 400


@app.route('/cargaUsuarios', methods=['POST'])
def cargaUsuarios():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    
    for elemento in raiz:
        id = elemento.attrib.get('id')
        password = elemento.attrib.get('password')
        nombre = elemento.find('nombre').text
        edad = int(elemento.find('edad').text)
        email = elemento.find('email').text
        telefono = elemento.find('telefono').text

        manager.addUsuario(id, nombre, edad, email, telefono, password)

        print(f'Usuario añadido: id={id}, nombre={nombre}, edad={edad}, email={email}, telefono={telefono}, password={password}')
    
    return jsonify({"message": "Archivo XML cargado correctamente"}), 200


@app.route('/verUsuarios', methods=['GET'])
def verUsuarios():
    u = manager.getUsuario()
    return jsonify(u), 200


@app.route('/cargaProductos', methods=['POST'])
def cargaProductos():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    
    for elemento in raiz:
        id = elemento.attrib.get('id')
        nombre = elemento.find('nombre').text
        precio = float(elemento.find('precio').text)
        descripcion = elemento.find('descripcion').text
        categoria = elemento.find('categoria').text
        cantidad = int(elemento.find('cantidad').text)
        imagen = elemento.find('imagen').text

        manager.addProducto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
        
        print(f'Producto añadido: id={id}, nombre={nombre}, precio={precio}, descripcion={descripcion}, categoria={categoria}, cantidad={cantidad}, imagen={imagen}')
    
    return jsonify({"message": "Archivo XML cargado correctamente"}), 200

@app.route('/verProductos', methods=['GET'])
def verProductos():
    v = manager.getProducto()
    return jsonify(v), 200


@app.route('/cargaEmpleados', methods=['POST'])
def cargaEmpleados():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    
    for elemento in raiz:
        codigo = elemento.attrib.get('codigo')
        nombre = elemento.find('nombre').text
        puesto = elemento.find('puesto').text

        manager.addEmpleado(codigo, nombre, puesto)
        
        print(f'Empleado añadido: codigo={codigo}, nombre={nombre}, puesto={puesto}')
    
    return jsonify({"message": "Archivo XML cargado correctamente"}), 200

@app.route('/verEmpleados', methods=['GET'])
def verEmpleados():
    x = manager.getEmpleado()
    return jsonify(x), 200

@app.route('/añadirCarrito', methods=['POST'])
def añadirCarrito():
    data = request.json
    user_id = data.get('user_id')
    product_ids = data.get('product_id')
    if manager.agregarCarrito(user_id, product_ids):
        return jsonify({"message": "Producto añadido al carrito"}), 200
    else:
        return jsonify({"message": "Error al añadir el producto al carrito"}), 500

@app.route('/verCarrito', methods=['GET'])
def verCarrito():
    user_id = request.args.get('user_id')
    print(f"Ver carrito para user_id: {user_id}") 
    carrito = manager.obtenerCarrito(user_id)
    return jsonify(carrito), 200

@app.route('/verListaCompras', methods=['GET'])
def verListaCompras():
    user_id = request.args.get('user_id')
    print(f"Ver lista de compras para user_id: {user_id}") 
    lista_compras = manager.obtenerListaCompras(user_id)
    return jsonify(lista_compras), 200

@app.route('/generarXMLCarrito', methods=['GET'])
def generarXMLCarrito():
    user_id = request.args.get('user_id')
    xml_tree = manager.generarXMLCarrito(user_id)
    xml_str = ET.tostring(xml_tree.getroot(), encoding='utf-8', method='xml')
    return Response(xml_str, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
