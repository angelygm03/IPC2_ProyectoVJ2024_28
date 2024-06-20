class Empleado:
    def __init__(self, codigo, nombre, puesto):
        self.codigo = codigo
        self.nombre = nombre
        self.puesto = puesto

    def obtener_nombre(self):
        return self.nombre