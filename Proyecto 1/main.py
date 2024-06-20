import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog, ttk
import xml.etree.ElementTree as ET
import re
import textwrap
from clases.usuario import Usuario
from lista_doble.lista_doble import ListaDoble
from clases.producto import Producto
from lista_dobleCircular.lista_dobleCircular import ListaDobleCircular
from clases.empleado import Empleado
from lista_circular.lista_circular import ListaCircularSimple
from lista_simple.lista_simple import ListaSimple
from pila.pila import Pila
from cola.cola import Cola
from clases.actividad import Actividad
from matriz_dispersa.matriz_dispersa import MatrizDispersa

# Inicializar las listas
usuarios = ListaDoble()
productos = ListaDobleCircular()
empleados = ListaCircularSimple()
carrito = Pila()
cola_solicitudes = Cola()
compras_aceptadas = ListaSimple()
actividades = MatrizDispersa()

# Función de autenticación de credenciales
def autenticacion(username, password):
    # Verificar si las credenciales corresponden al administrador
    if username == admin_username and password == admin_password:
        return 'admin'
    
    # Buscar en la lista de usuarios
    actual = usuarios.cabeza
    while actual is not None:
        if actual.usuario.id == username and actual.usuario.password == password:
            return actual.usuario
        actual = actual.siguiente
    return None

# Función para la ventana de administrador
def admin_window():
    
    # Función para cargar usuarios desde uno o más archivos XML
    def cargar_usuarios():
        file_paths = filedialog.askopenfilenames(
            filetypes=[("XML files", "*.xml")],
            title="Seleccionar archivos XML"
        )
        if file_paths:
            try:
                for file_path in file_paths:
                    print("Cargando usuarios desde:", file_path)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    for user in root.findall('usuario'):
                        user_id = user.get('id')
                        password = user.get('password')
                        nombre = user.find('nombre').text
                        edad = int(user.find('edad').text)
                        email = user.find('email').text
                        telefono = user.find('telefono').text

                        # Validaciones
                        if usuarios.buscar_por_id(user_id) is not None:
                            raise ValueError(f"El ID {user_id} ya existe.")
                        
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            raise ValueError(f"Email {email} no es válido.")

                        if not telefono.isdigit() or len(telefono) != 8:
                            raise ValueError(f"Teléfono {telefono} no es válido. Debe contener 8 dígitos.")

                        # Crear y agregar el usuario a la lista doblemente enlazada
                        nuevo_usuario = Usuario(user_id, nombre, edad, email, telefono, password)
                        usuarios.insertar(nuevo_usuario)
                        print(f"Usuario {user_id} cargado correctamente.")
                        
                # Mostrar en consola los usuarios cargados
                usuarios.imprimir_usuarios()

                messagebox.showinfo("Éxito", "Usuarios cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Función para generar reporte de usuarios
    def reporte_usuarios():
        print("Generando reporte de usuarios...")  
        usuarios.graficar()
        print("Reporte de usuarios generado.")

    # Función para cargar productos desde uno o más archivos XML
    def cargar_productos():
        file_paths = filedialog.askopenfilenames(
            filetypes=[("XML files", "*.xml")],
            title="Seleccionar archivos XML"
        )
        if file_paths:
            try:
                for file_path in file_paths:
                    print("Cargando productos desde:", file_path)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    for product in root.findall('producto'):
                        id = product.get('id')
                        nombre = product.find('nombre').text
                        precio = float(product.find('precio').text.replace(',', ''))
                        descripcion = product.find('descripcion').text
                        categoria = product.find('categoria').text
                        cantidad = int(product.find('cantidad').text)
                        imagen = product.find('imagen').text

                        # Crear y agregar el producto a la lista circular doblemente enlazada
                        nuevo_producto = Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
                        productos.agregar(nuevo_producto)
                        print(f"Producto {id} cargado correctamente.")

                # Mostrar en consola los productos cargados
                productos.imprimir()

                messagebox.showinfo("Éxito", "Productos cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Función para generar reporte de productos
    def reporte_productos():
        print("Generando reporte de productos...")  
        productos.graficar()
        print("Reporte de productos generado.")

    # Función para cargar empleados desde archivos XML
    def cargar_empleados():
        file_paths = filedialog.askopenfilenames(
            filetypes=[("XML files", "*.xml")],
            title="Seleccionar archivos XML"
        )
        if file_paths:
            try:
                for file_path in file_paths:
                    print("Cargando empleados desde:", file_path)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    for empleado_elem in root.findall('empleado'):
                        codigo = empleado_elem.get('codigo')
                        nombre = empleado_elem.find('nombre').text
                        puesto = empleado_elem.find('puesto').text

                        # Crear y agregar el empleado a la lista circular simplemente enlazada
                        nuevo_empleado = Empleado(codigo, nombre, puesto)
                        empleados.agregar(nuevo_empleado)
                        print(f"Empleado {codigo} cargado correctamente.")
                        
                # Mostrar en consola los empleados cargados
                empleados.imprimir()

                messagebox.showinfo("Éxito", "Empleados cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def dias_de_la_semana(dia_semana):
        if dia_semana == 1:
            return "lunes"
        elif dia_semana == 2:
            return "martes"
        elif dia_semana == 3:
            return "miércoles"
        elif dia_semana == 4:
            return "jueves"
        elif dia_semana == 5:
            return "viernes"
        elif dia_semana == 6:
            return "sábado"
        elif dia_semana == 7:
            return "domingo"
        else:
            return "Día no válido"
    
    #Función para cargar y parsear el xml de actividades
    def cargar_actividades():
        file_paths = filedialog.askopenfilenames(
            filetypes=[("XML files", "*.xml")],
            title="Seleccionar archivos XML"
        )
        if file_paths:
            try:
                for file_path in file_paths:
                    print("Cargando actividades desde:", file_path)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    for actividad in root.findall('actividad'):
                        id = actividad.get('id')
                        nombre = actividad.find('nombre').text
                        descripcion = actividad.find('descripcion').text

                        # Obtener día de la semana y hora
                        dia = actividad.find('dia')
                        if dia is None:
                            raise ValueError("El elemento <dia> no está definido para la actividad.")
                        
                        dia_semana = int(dia.text)
                        hora = int(dia.get('hora'))

                        # Convertir el día de la semana a nombre
                        dia_nombre = dias_de_la_semana(dia_semana)

                        # Obtener el nombre del empleado asignado a la actividad mediante la lista circular
                        empleado_id = actividad.find('empleado').text
                        empleado_nombre = empleados.obtener_nombre(empleado_id)

                        # Insertar actividad en la matriz dispersa
                        dato_actividad = f"{id}, {nombre}, {empleado_nombre}, {dia_nombre}, {hora} hrs."
                        actividades.insertar(hora, dia_semana, dato_actividad)
                        print(f"Actividad {id} cargada correctamente.")
                    
                    actividades.imprimir()

                messagebox.showinfo("Éxito", "Actividades cargadas correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))


    # Función para generar reporte de empleados
    def reporte_empleados():
        print("Generando reporte de empleados...")  
        empleados.graficar()
        print("Reporte de empleados generado.")

    # Función para generar reporte de compras
    def reporte_compras():
        print("Generando reporte de compras...")  
        compras_aceptadas.graficar()
        print("Reporte de compras generado.")
    
    #Función para generar reporte de solicitudes de compra
    def reporte_solicitudes():
        print("Generando reporte de solicitudes de compra...")  
        cola_solicitudes.graficar()
        print("Reporte de solicitudes de compra generado.")
    
    #Función para generar reporte de actividades
    def reporte_actividades():
        print("Generando reporte de actividades...")  
        actividades.graficar()
        print("Reporte de actividades generado.")

    admin_win = tk.Toplevel()
    admin_win.title("Ventana de Administrador")
    admin_win.geometry("900x450")
    admin_win.configure(bg="#26355D")

    # Menú de opciones
    menu_opciones = tk.Menu(admin_win)
    admin_win.config(menu=menu_opciones)

    # Frame para mostrar la cola de solicitudes de compra
    cola_frame = tk.Frame(admin_win, bg="#26355D")
    cola_frame.pack(pady=10)

    # Text area para mostrar las solicitudes de compra
    solicitudes_text = tk.Text(cola_frame, height=15, width=80, font=("Verdana", 12), fg="#FFFFFF", bg="#3B4C7A")
    solicitudes_text.pack(padx=10, pady=10)

    # Botón para actualizar la lista de solicitudes
    def actualizar_solicitudes():
        solicitudes_text.delete(1.0, tk.END) 
        cola_solicitudes.mostrar_en_text_area(solicitudes_text)

    actualizar_button = tk.Button(cola_frame, text="Actualizar Solicitudes", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=actualizar_solicitudes)
    actualizar_button.pack(pady=10)

    def aceptar_solicitud():
        solicitud = cola_solicitudes.dequeue()
        if solicitud:
            # Extraer los atributos del nodo solicitud
            usuario_id = solicitud.id_usuario
            nombre_usuario = solicitud.nombre_usuario
            productos = solicitud.productos
            total = solicitud.total
            
            # Insertar en la lista de compras aceptadas
            compras_aceptadas.insertar(usuario_id, nombre_usuario, productos, total)
            print("Solicitud aceptada:")
            compras_aceptadas.mostrar()
            actualizar_solicitudes()


    def rechazar_solicitud():
        solicitud = cola_solicitudes.dequeue()
        if solicitud:
            print("Solicitud rechazada.")
            actualizar_solicitudes()

    # Botones Aceptar y Rechazar
    botones_frame = tk.Frame(admin_win, bg="#26355D")
    botones_frame.pack(pady=10)

    aceptar_button = tk.Button(botones_frame, text="Aceptar", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=aceptar_solicitud)
    aceptar_button.grid(row=0, column=0, padx=10)

    rechazar_button = tk.Button(botones_frame, text="Rechazar", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=rechazar_solicitud)
    rechazar_button.grid(row=0, column=1, padx=10)
    actualizar_solicitudes()

    # Opción Archivo
    submenu_archivo = tk.Menu(menu_opciones, tearoff=0)
    menu_opciones.add_cascade(label="Cargar", menu=submenu_archivo)
    submenu_archivo.add_command(label="Cargar usuarios", command=cargar_usuarios)
    submenu_archivo.add_separator()
    submenu_archivo.add_command(label="Cargar productos ", command=cargar_productos)
    submenu_archivo.add_separator()
    submenu_archivo.add_command(label="Cargar empleados", command=cargar_empleados)
    submenu_archivo.add_separator()
    submenu_archivo.add_command(label="Cargar actividades", command=cargar_actividades)
    
    # Opción Reportes
    submenu_reportes = tk.Menu(menu_opciones, tearoff=0)
    menu_opciones.add_cascade(label="Reportes", menu=submenu_reportes)
    submenu_reportes.add_command(label="Reporte de usuario", command=reporte_usuarios)
    submenu_reportes.add_separator()
    submenu_reportes.add_command(label="Reporte de productos", command=reporte_productos)
    submenu_reportes.add_separator()
    submenu_reportes.add_command(label="Reporte de empleados", command=reporte_empleados)
    submenu_reportes.add_separator()
    submenu_reportes.add_command(label="Reporte de solicitudes", command=reporte_solicitudes)
    submenu_reportes.add_separator()
    submenu_reportes.add_command(label="Reporte de compras", command=reporte_compras)
    submenu_reportes.add_separator()
    submenu_reportes.add_command(label="Reporte de actividades", command=reporte_actividades)

    # Botón de salir
    #exit_button = tk.Button(admin_win, text="Salir", font=("Comic Sans MS", 14), bg="#4D5F91", fg="#FFFFFF", command=admin_win.destroy)
    #exit_button.pack(pady=10)

def cargar_imagen(imagen_path, width, height):
    imagen_original = Image.open(imagen_path)
    imagen_redimensionada = imagen_original.resize((width, height))
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
    return imagen_tk

# Función para la ventana de usuario
def user_window(usuario):

    def ver_producto():
        cursor_pos = text_area.index(tk.INSERT)
        current_line = int(cursor_pos.split('.')[0])
        producto_seleccionado = text_area.get(f"{current_line}.0", f"{current_line}.end").strip()
        if producto_seleccionado:
            actual = productos.primero
            while actual is not None:
                producto = actual.producto
                if producto.nombre == producto_seleccionado:
                    label_nombre.config(text=f"Nombre: {producto.nombre}")
                    descripcion_formateada = textwrap.fill(producto.descripcion, width=50)
                    label_descripcion.config(text=f"Descripción:\n{descripcion_formateada}")
                    label_categoria.config(text=f"Categoría: {producto.categoria}")
                    label_cantidad.config(text=f"Cantidad disponible: {producto.cantidad}")
                    label_precio.config(text=f"Precio: Q{producto.precio}")

                    # Redimensionar y cargar la imagen
                    imagen_path = producto.imagen
                    imagen_tk = cargar_imagen(imagen_path, 200, 200)

                    # Mostrar la imagen en el label
                    label_imagen.config(image=imagen_tk)
                    label_imagen.image = imagen_tk
                    break
                actual = actual.siguiente
                if actual == productos.primero:
                    break
        else:
            messagebox.showwarning("Error", "Por favor, seleccione un producto primero.")

    def agregar_al_carrito():
        cantidad = cantidad_entry.get()
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showwarning("Error", "Ingrese una cantidad válida.")
            return

        cantidad = int(cantidad)
        producto_seleccionado = label_nombre.cget("text").replace("Nombre: ", "").strip()
        
        if not producto_seleccionado:
            messagebox.showwarning("Error", "Seleccione un producto primero.")
            return

        actual = productos.primero
        while actual is not None:
            producto = actual.producto
            if producto.nombre == producto_seleccionado:
                if cantidad > producto.cantidad:
                    messagebox.showwarning("Error", "Cantidad no disponible.")
                    return
                else:
                    carrito.push(producto.nombre, producto.precio, cantidad)
                    carrito.mostrar()
                    messagebox.showinfo("Éxito", f"{producto.nombre} agregado al carrito.")
                    return
            actual = actual.siguiente
            if actual == productos.primero:
                break

    def ver_carrito():
        if carrito.isEmpty():
            messagebox.showinfo("Carrito vacío", "No hay productos en el carrito.")
            return
        carrito.graficar(usuario.id)

    def confirmar_compra():
        if carrito.isEmpty():
            messagebox.showwarning("Error", "No has agregado productos.")
            return
        
        productos_compra = ""
        total = 0
        while not carrito.isEmpty():
            producto = carrito.pop()
            productos_compra += f"Producto: {producto.nombre_producto}, Precio: {producto.precio_producto}, Cantidad: {producto.cantidad_producto} \n"
            total += round(producto.precio_producto * producto.cantidad_producto, 2)
        cola_solicitudes.enqueue(usuario.id, usuario.nombre, productos_compra, total)
        print("Compra confirmada, productos en la cola de solicitudes:")
        cola_solicitudes.mostrar() 
        messagebox.showinfo("Solicitud en proceso", "Tu compra se encuentra en proceso, por favor espera.")

    user_win = tk.Toplevel()
    user_win.title("Bienvenido a IPCmarket")
    user_win.geometry("1100x600")
    user_win.configure(bg="#26355D")

    tk.Label(user_win, text=f"Bienvenido, {usuario.nombre}", font=("Comic Sans MS", 16), bg="#26355D", fg="#FFFFFF").pack(pady=20)

    # Marco para la lista de productos y detalles
    frame = tk.Frame(user_win, bg="#26355D")
    frame.pack(pady=20, padx=10, side=tk.LEFT)

    # Crear un text area para los productos
    text_area = tk.Text(frame, height=20, width=35, font=("Verdana", 12), fg="#FFFFFF", bg="#3B4C7A")
    text_area.pack(side=tk.LEFT, padx=10)

    # Agregar los nombres de los productos al text area
    actual = productos.primero
    while actual is not None:
        producto = actual.producto
        text_area.insert(tk.END, f"{producto.nombre}\n")
        actual = actual.siguiente
        if actual == productos.primero:
            break

    # Configurar el text area como solo de lectura después de agregar los productos
    text_area.configure(state="disabled")

    # Labels para mostrar los detalles del producto seleccionado
    label_nombre = tk.Label(frame, text="", font=("Verdana", 12), bg="#26355D", fg="#FFFFFF", anchor="w", padx=10)
    label_nombre.pack(pady=5)
    label_precio = tk.Label(frame, text="", font=("Verdana", 12), bg="#26355D", fg="#FFFFFF", anchor="w", padx=10)
    label_precio.pack(pady=5)
    label_descripcion = tk.Label(frame, text="", font=("Verdana", 12), bg="#26355D", fg="#FFFFFF", anchor="w", padx=10)
    label_descripcion.pack(pady=5)
    label_categoria = tk.Label(frame, text="", font=("Verdana", 12), bg="#26355D", fg="#FFFFFF", anchor="w", padx=10)
    label_categoria.pack(pady=5)
    label_cantidad = tk.Label(frame, text="", font=("Verdana", 12), bg="#26355D", fg="#FFFFFF", anchor="w", padx=10)
    label_cantidad.pack(pady=5)

    # Botón para ver producto
    ver_button = tk.Button(frame, text="Ver Producto", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=ver_producto)
    ver_button.pack(pady=10)

    # Label y entrada de texto para la cantidad
    cantidad_label = tk.Label(frame, text="Cantidad a agregar al carrito:", font=("Comic Sans MS", 12), bg="#26355D", fg="#FFFFFF")
    cantidad_label.pack(pady=5)
    cantidad_entry = tk.Entry(frame, font=("Verdana", 12), bg="#3B4C7A", fg="#FFFFFF")
    cantidad_entry.pack(pady=5)

    # Marco para la imagen del producto
    image_frame = tk.Frame(user_win, bg="#26355D")
    image_frame.pack(pady=20, padx=10, side=tk.RIGHT)

    # Label para mostrar la imagen del producto
    label_imagen = tk.Label(image_frame, bg="#26355D")
    label_imagen.pack(pady=10)

    # Botón para agregar al carrito
    agregar_carrito_button = tk.Button(frame, text="Agregar al Carrito", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=agregar_al_carrito)
    agregar_carrito_button.pack(pady=10, side=tk.LEFT)

    # Botón para ver carrito
    ver_carrito_button = tk.Button(frame, text="Ver Carrito", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=ver_carrito)
    ver_carrito_button.pack(pady=10, side=tk.LEFT)

    # Botón para confirmar compra
    confirmar_compra_button = tk.Button(frame, text="Confirmar Compra", font=("Comic Sans MS", 12), bg="#4D5F91", fg="#FFFFFF", command=confirmar_compra)
    confirmar_compra_button.pack(pady=10, side=tk.LEFT)


# Credenciales del administrador
admin_username = 'AdminIPC2'
admin_password = 'IPC2VJ2024'

# Función de inicio de sesión
def login():
    username = entry_username.get()
    password = entry_password.get()
    user = autenticacion(username, password)
    
    if user:
        print("Inicio de sesión como usuario exitoso.")
        if user == 'admin':
            admin_window()
        else:
            user_window(user)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Ventana principal
root = tk.Tk()
root.title("IPCmarket")
root.geometry("600x300")
root.configure(bg="#26355D")

# Estilo
bg_color = "#26355D"
fg_color = "#FFFFFF"
entry_bg = "#3B4C7A"
button_bg = "#4D5F91"
button_fg = "#FFFFFF"

# Etiqueta del título
title_label = tk.Label(root, text="Iniciar Sesión", font=("Comic Sans MS", 24), bg=bg_color, fg=fg_color)
title_label.pack(pady=20)

# Marco para los campos de entrada
frame = tk.Frame(root, bg=bg_color)
frame.pack(pady=20)

# Campo de nombre de usuario
username_label = tk.Label(frame, text="Usuario", font=("Comic Sans MS", 14), bg=bg_color, fg=fg_color)
username_label.grid(row=0, column=0, pady=10, padx=10)
entry_username = tk.Entry(frame, font=("Verdana", 14), bg=entry_bg, fg=fg_color, insertbackground=fg_color)
entry_username.grid(row=0, column=1, pady=10, padx=10)

# Campo de contraseña
password_label = tk.Label(frame, text="Contraseña", font=("Comic Sans MS", 14), bg=bg_color, fg=fg_color)
password_label.grid(row=1, column=0, pady=10, padx=10)
entry_password = tk.Entry(frame, font=("Verdana", 14), show="*", bg=entry_bg, fg=fg_color, insertbackground=fg_color)
entry_password.grid(row=1, column=1, pady=10, padx=10)

# Botón de login
login_button = tk.Button(root, text="Ingresar", font=("Comic Sans MS", 14), bg=button_bg, fg=button_fg, command=login, width=14, height=2)
login_button.pack(pady=18)

# Ejecutar la aplicación
root.mainloop()
