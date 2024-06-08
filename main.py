import tkinter as tk
from tkinter import messagebox

# Función de autenticación simulada
def authenticate(username, password):
    if username == "AdminIPC2" and password == "IPC2VJ2024":
        return True
    else:
        return False

# Función que maneja el ingreso o login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if authenticate(username, password):
        messagebox.showinfo("Login exitoso", "Bienvenido!")
    else:
        messagebox.showerror("Error de login", "Nombre de usuario o contraseña incorrectos")

# Ventana principal
root = tk.Tk()
root.title("Login Moderno")
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
