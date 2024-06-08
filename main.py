import tkinter as tk
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as ET
import re
from clases.usuario import Usuario
from lista_doble.lista_doble import ListaDoble

# Inicializar las listas
usuarios = ListaDoble()

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

# Función de autenticación de credenciales
def autenticacion(username, password):
    actual = usuarios.cabeza
    while actual is not None:
        if actual.usuario.id == username and actual.usuario.password == password:
            return actual.usuario
        actual = actual.siguiente
    return None

# Función para la ventana de administrador
def admin_window():
    admin_win = tk.Toplevel()
    admin_win.title("Ventana de Administrador")
    admin_win.geometry("600x300")
    admin_win.configure(bg="#26355D")

    # Botón de cargar usuarios
    cargar_usuarios_button = tk.Button(admin_win, text="Cargar Usuarios", font=("Comic Sans MS", 14), bg=button_bg, fg=button_fg, command=cargar_usuarios)
    cargar_usuarios_button.pack(pady=10)

    # Botón de salir
    exit_button = tk.Button(admin_win, text="Salir", font=("Comic Sans MS", 14), bg=button_bg, fg=button_fg, command=admin_win.destroy)
    exit_button.pack(pady=10)

# Función para la ventana de usuario
def user_window(usuario):
    user_win = tk.Toplevel()
    user_win.title("Ventana de Usuario")
    user_win.geometry("600x300")
    user_win.configure(bg="#26355D")

    # ventana de usuario (pendiente de editar)
    tk.Label(user_win, text=f"Bienvenido, {usuario.nombre}", font=("Comic Sans MS", 16)).pack(pady=20)

# Función de inicio de sesión
def login():
    username = entry_username.get()
    password = entry_password.get()
    user = autenticacion(username, password)
    
    if user:
        print("Inicio de sesión como usuario exitoso.")
        if user.id == 'admin':
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

# Añadir usuario administrador por defecto
admin_usuario = Usuario('admin', 'Admin', 0, 'admin@example.com', '00000000', 'admin')
usuarios.insertar(admin_usuario)

# Ejecutar la aplicación
root.mainloop()
