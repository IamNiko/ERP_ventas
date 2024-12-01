import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from tkinter import Menu
import sqlite3
from usuarios import GestionUsuarios

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("dark-blue")  # Tema predeterminado

# Clase para la pantalla de inicio de sesión
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GoUp BI ERP - Login")
        self.geometry("400x500")

        # Cargar el logo
        logo_image = Image.open("img/gub.png")
        self.logo_image = CTkImage(light_image=logo_image, size=(300, 200))

        # Configurar el logo
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.pack(pady=20)

        # Campo de usuario
        self.username_label = ctk.CTkLabel(self, text="Usuario:", font=("Arial", 14))
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu usuario")
        self.username_entry.pack(pady=5)

        # Campo de contraseña
        self.password_label = ctk.CTkLabel(self, text="Contraseña:", font=("Arial", 14))
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña", show="*")
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self, text="Iniciar sesión", command=self.validate_login)
        self.login_button.pack(pady=20)

        # Asociar el evento Enter al botón de inicio de sesión
        self.bind("<Return>", lambda event: self.validate_login())

        # Etiqueta para mensajes de error
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

    def validate_login(self):
        """Valida las credenciales de inicio de sesión."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Conectar a la base de datos
        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()

        # Verificar las credenciales en la base de datos
        cursor.execute('''
            SELECT rol FROM usuarios WHERE nombre_usuario = ? AND contrasena = ? AND activo = 1
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            rol = user[0]
            self.error_label.configure(text="¡Inicio de sesión exitoso!", text_color="green")
            self.destroy()
            MainApp(rol).mainloop()  # Inicia la ventana principal con el rol
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos", text_color="red")

# Clase principal de la aplicación
class MainApp(ctk.CTk):
    def __init__(self, rol):
        super().__init__()
        self.title("GoUp BI ERP - Principal")
        self.geometry("800x600")
        self.rol = rol

        # Configurar el menú y la interfaz
        self.configurar_menu()
        self.configurar_interfaz()

    def configurar_menu(self):
        """Configura el menú principal."""
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Menú Archivo
        archivo_menu = Menu(self.menu_bar, tearoff=0)
        archivo_menu.add_command(label="Logout", command=self.logout)
        archivo_menu.add_command(label="Salir", command=self.destroy)
        self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        

        # Menús según el rol
        if self.rol in ['administrador', 'vendedor']:
            self.configurar_menu_facturacion()
        if self.rol in ['administrador', 'almacen']:
            self.configurar_menu_stock()
        if self.rol == 'administrador':
            self.configurar_menu_usuarios()

    def configurar_menu_facturacion(self):
        facturacion_menu = Menu(self.menu_bar, tearoff=0)
        facturacion_menu.add_command(label="Nueva factura", command=self.nueva_factura)
        self.menu_bar.add_cascade(label="Facturación", menu=facturacion_menu)

    def configurar_menu_stock(self):
        stock_menu = Menu(self.menu_bar, tearoff=0)
        stock_menu.add_command(label="Ver stock", command=self.ver_stock)
        self.menu_bar.add_cascade(label="Stock", menu=stock_menu)

    def configurar_menu_usuarios(self):
        usuarios_menu = Menu(self.menu_bar, tearoff=0)
        usuarios_menu.add_command(label="Gestionar Usuarios", command=self.abrir_gestion_usuarios)
        self.menu_bar.add_cascade(label="Usuarios", menu=usuarios_menu)

    def configurar_interfaz(self):
        """Configura la interfaz basada en el rol del usuario."""
        if self.rol == 'administrador':
            self.label = ctk.CTkLabel(self, text="Acceso total al sistema", font=("Arial", 16, "bold"))
        elif self.rol == 'vendedor':
            self.label = ctk.CTkLabel(self, text="Acceso a facturación y ventas", font=("Arial", 16, "bold"))
        elif self.rol == 'almacen':
            self.label = ctk.CTkLabel(self, text="Acceso al control de stock", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)


    def abrir_gestion_usuarios(self):
        """Abre la gestión de usuarios asegurándose de no duplicar vistas."""
        # Verifica si ya existe una instancia y la elimina
        if hasattr(self, 'gestion_usuarios_frame'):
            self.gestion_usuarios_frame.destroy()

        # Crea una nueva instancia y la muestra
        self.gestion_usuarios_frame = GestionUsuarios(self)
        self.gestion_usuarios_frame.pack(fill="both", expand=True)

    def logout(self):
        """Cierra la sesión y vuelve al login."""
        self.destroy()
        LoginApp().mainloop()

    def nueva_factura(self):
        print("Abrir interfaz de nueva factura.")

    def ver_stock(self):
        print("Abrir interfaz de control de stock.")

    def clear_interface(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.winfo_children():
            widget.destroy()


# Iniciar la app
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
