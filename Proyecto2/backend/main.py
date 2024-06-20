from flask import Flask, request
from flask.json import jsonify
from xml.etree import ElementTree as ET
from manage import Manager

app = Flask(__name__)
manager = Manager()

@app.route('/')
def index():
    return "API con Python y Flask funcionando correctamente"

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
