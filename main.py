import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from tkinter import Menu
import sqlite3
from usuarios import GestionUsuarios
from gestion_articulos import GestionArticulos
from nueva_factura import NuevaFactura
from facturacion import HistoricoVentas, BuscadorVentas

# Configuración inicial de CustomTkinter
ctk.set_default_color_theme("dark-blue")  # Opcional, pero mejora la visibilidad
ctk.set_appearance_mode("dark")  # Apariencia oscura

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
        self.geometry("1200x800")  # Ajustado para pantallas de portátil
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

        # Menú Clientes
        self.configurar_menu_clientes()

            # Menú Artículos
        self.configurar_menu_articulos()

                # Menú Facturación
        self.configurar_menu_facturacion()

    def configurar_menu_articulos(self):
        """Configura el menú Artículos."""
        articulos_menu = Menu(self.menu_bar, tearoff=0)
        articulos_menu.add_command(label="Gestionar Artículos", command=self.ver_articulos)
        self.menu_bar.add_cascade(label="Artículos", menu=articulos_menu)


    def configurar_menu_facturacion(self):
        facturacion_menu = Menu(self.menu_bar, tearoff=0)
        facturacion_menu.add_command(label="Nueva factura", command=self.nueva_factura)
        facturacion_menu.add_command(label="Histórico de Ventas", command=self.historico_ventas)
        self.menu_bar.add_cascade(label="Facturación", menu=facturacion_menu)

    def nueva_factura(self):
        print("Abrir interfaz de nueva factura.")



    def configurar_menu_stock(self):
        stock_menu = Menu(self.menu_bar, tearoff=0)
        stock_menu.add_command(label="Ver stock", command=self.ver_stock)
        self.menu_bar.add_cascade(label="Stock", menu=stock_menu)

    def configurar_menu_usuarios(self):
        usuarios_menu = Menu(self.menu_bar, tearoff=0)
        usuarios_menu.add_command(label="Gestionar Usuarios", command=self.abrir_gestion_usuarios)
        self.menu_bar.add_cascade(label="Usuarios", menu=usuarios_menu)

    def configurar_menu_clientes(self):
        clientes_menu = Menu(self.menu_bar, tearoff=0)
        clientes_menu.add_command(label="Ver Clientes", command=self.ver_clientes)
        clientes_menu.add_command(label="Agregar Cliente", command=self.agregar_cliente)
        self.menu_bar.add_cascade(label="Clientes", menu=clientes_menu)

    def configurar_menu_facturacion(self):
        facturacion_menu = Menu(self.menu_bar, tearoff=0)
        facturacion_menu.add_command(label="Nueva factura", command=self.nueva_factura)
        facturacion_menu.add_command(label="Buscar Ventas", command=self.abrir_buscador_ventas)
        self.menu_bar.add_cascade(label="Facturación", menu=facturacion_menu)
    def abrir_buscador_ventas(self):
        """Abrir el buscador de ventas en la ventana principal."""
        if hasattr(self, 'buscador_ventas_frame'):
            self.buscador_ventas_frame.destroy()

        self.buscador_ventas_frame = BuscadorVentas(self)




    def configurar_interfaz(self):
        """Configura la interfaz basada en el rol del usuario."""
        # Limpia los widgets existentes
        self.clear_interface()

        # Contenedor principal para organizar elementos
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Panel lateral derecho para botones
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar_frame.pack(side="right", fill="y", padx=20, pady=20)

        # Contenedor central para el contenido principal
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Botón "Inicio"
        self.boton_inicio = ctk.CTkButton(
            self.sidebar_frame, text="Inicio", command=self.configurar_interfaz, width=100, height=100, font=("Arial", 14)
        )
        self.boton_inicio.pack(pady=15)

        # Botón "Nueva Factura"
        self.boton_factura = ctk.CTkButton(
            self.sidebar_frame, text="Nueva Factura", command=self.nueva_factura, width=100, height=100, font=("Arial", 14)
        )
        self.boton_factura.pack(pady=15)

        # Botón "Artículos"
        self.boton_articulos = ctk.CTkButton(
            self.sidebar_frame, text="Artículos", command=self.ver_articulos, width=100, height=100, font=("Arial", 14)
        )
        self.boton_articulos.pack(pady=15)

        # Contenido principal inicial
        self.mostrar_pantalla_principal()

    def mostrar_pantalla_principal(self):
        """Muestra el contenido principal de la pantalla inicial."""
        # Limpia el contenedor de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Contenido principal (texto central)
        if self.rol == 'administrador':
            self.label = ctk.CTkLabel(self.content_frame, text="Acceso total al sistema", font=("Arial", 18, "bold"))
        elif self.rol == 'vendedor':
            self.label = ctk.CTkLabel(self.content_frame, text="Acceso a facturación y ventas", font=("Arial", 18, "bold"))
        elif self.rol == 'almacen':
            self.label = ctk.CTkLabel(self.content_frame, text="Acceso al control de stock", font=("Arial", 18, "bold"))
        self.label.pack(pady=30)

    def abrir_gestion_usuarios(self):
        """Muestra la interfaz de gestión de usuarios en el marco de contenido."""
        # Limpia el contenedor de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Muestra el contenido de la gestión de usuarios
        self.gestion_usuarios_frame = GestionUsuarios(self.content_frame)
        self.gestion_usuarios_frame.pack(fill="both", expand=True)

    def logout(self):
        """Cierra la sesión y vuelve al login."""
        self.destroy()
        LoginApp().mainloop()

    def nueva_factura(self):
        print("Abrir interfaz de nueva factura.")

    def ver_stock(self):
        print("Abrir interfaz de control de stock.")

    def ver_articulos(self):
        """Abre la gestión de artículos en el marco principal."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        gestion_articulos = GestionArticulos(self.content_frame)
        gestion_articulos.pack(fill="both", expand=True)


    def ver_clientes(self):
        print("Abrir interfaz para ver clientes.")

    def agregar_cliente(self):
        print("Abrir interfaz para agregar cliente.")

    def clear_interface(self):
        """Elimina todos los widgets de la ventana principal, excepto el menú."""
        for widget in self.winfo_children():
            if isinstance(widget, Menu):
                continue
            widget.destroy()
# Configurar fuentes globales
FONT_BASE = ("Arial", 16)
FONT_TITLE = ("Arial", 20, "bold")
FONT_BUTTON = ("Arial", 14)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP Ventas")
        
        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Ajustar el tamaño inicial de la ventana
        self.geometry(f"{int(screen_width * 0.9)}x{int(screen_height * 0.9)}")

        # Configurar escalado general
        scale_factor = screen_width / 1920  # Basado en una resolución estándar
        self.scaling_widgets(scale_factor)

        # Crear elementos básicos (puedes agregar más botones o frames aquí)
        label = ctk.CTkLabel(self, text="ERP de Ventas", font=FONT_TITLE)
        label.pack(pady=20)

        # Botón para acceder a la gestión de artículos
        button_articulos = ctk.CTkButton(self, text="Gestión de Artículos", command=self.abrir_gestion_articulos, font=FONT_BUTTON, width=200, height=50)
        button_articulos.pack(pady=20)

    def scaling_widgets(self, factor):
        """Escala fuentes y tamaños en función del factor de escala."""
        global FONT_BASE, FONT_TITLE, FONT_BUTTON
        FONT_BASE = ("Arial", int(16 * factor))
        FONT_TITLE = ("Arial", int(20 * factor), "bold")
        FONT_BUTTON = ("Arial", int(14 * factor))

    def abrir_gestion_articulos(self):
        """Abrir la ventana de gestión de artículos."""
        gestion_articulos = GestionArticulos(self)
        gestion_articulos.pack(fill="both", expand=True)

# Iniciar la app
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
