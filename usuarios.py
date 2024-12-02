import customtkinter as ctk
import sqlite3
from tkinter import messagebox


class GestionUsuarios(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.conn = sqlite3.connect("erp_ventas.db")
        self.cursor = self.conn.cursor()

        # Variable para almacenar el usuario seleccionado
        self.selected_user_id = ctk.IntVar(value=0)

        # Botones de acciones
        self.botones_frame = ctk.CTkFrame(self)
        self.botones_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(self.botones_frame, text="Agregar Usuario", command=self.abrir_agregar_usuario).pack(side="left", padx=5)
        ctk.CTkButton(self.botones_frame, text="Editar Usuario", command=self.abrir_editar_usuario).pack(side="left", padx=5)

        # Tabla de usuarios con barra de desplazamiento
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=400)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Actualizar la tabla al iniciar
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Actualiza la tabla de usuarios, asegurándose de que no haya duplicaciones."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Encabezados de la tabla
        headers = ["Seleccionar", "ID", "Usuario", "Rol", "Activo", "Eliminar"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5)

        # Datos de la tabla
        self.cursor.execute("SELECT id, usuario, rol, activo FROM usuarios")
        usuarios = self.cursor.fetchall()

        for row, usuario in enumerate(usuarios, start=1):
            # Botón de selección
            ctk.CTkRadioButton(
                self.scrollable_frame,
                variable=self.selected_user_id,
                value=usuario[0]
            ).grid(row=row, column=0, padx=5, pady=5)

            # Datos
            for col, value in enumerate(usuario, start=1):
                ctk.CTkLabel(self.scrollable_frame, text=str(value)).grid(row=row, column=col, padx=5, pady=5)

            # Botón de eliminar
            ctk.CTkButton(
                self.scrollable_frame,
                text="Eliminar",
                command=lambda user_id=usuario[0]: self.confirmar_eliminar_usuario(user_id)
            ).grid(row=row, column=4, padx=5, pady=5)

    def abrir_agregar_usuario(self):
        """Abre la interfaz para agregar un usuario y actualiza la tabla al cerrar."""
        ventana_agregar = AgregarUsuario(self)
        self.wait_window(ventana_agregar)  # Espera a que la ventana se cierre
        self.actualizar_tabla()  # Actualiza la tabla al cerrar la ventana

    def abrir_editar_usuario(self):
        """Abre la interfaz para editar el usuario seleccionado."""
        if self.selected_user_id.get() != 0:
            ventana_editar = EditarUsuario(self, usuario_id=self.selected_user_id.get())
            self.wait_window(ventana_editar)  # Espera a que la ventana se cierre
            self.actualizar_tabla()  # Actualiza la tabla al cerrar la ventana
        else:
            messagebox.showinfo("Información", "Por favor selecciona un usuario para editar.")

    def confirmar_eliminar_usuario(self, user_id):
        """Muestra una ventana de confirmación antes de eliminar un usuario."""
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm:
            self.eliminar_usuario(user_id)

    def eliminar_usuario(self, user_id):
        """Elimina un usuario de la base de datos."""
        self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        self.conn.commit()
        self.actualizar_tabla()


class AgregarUsuario(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Agregar Usuario")
        self.geometry("400x300")

        # Asegurar que la ventana esté al frente
        self.lift()
        self.grab_set()
        self.focus_set()

        # Campos
        ctk.CTkLabel(self, text="Nombre de Usuario:").pack(pady=5)
        self.nombre_entry = ctk.CTkEntry(self)
        self.nombre_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Contraseña:").pack(pady=5)
        self.contrasena_entry = ctk.CTkEntry(self, show="*")
        self.contrasena_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Rol:").pack(pady=5)
        self.rol_var = ctk.StringVar(value="vendedor")
        self.rol_dropdown = ctk.CTkOptionMenu(self, variable=self.rol_var, values=["administrador", "vendedor", "almacen"])
        self.rol_dropdown.pack(pady=5)

        ctk.CTkButton(self, text="Guardar", command=self.guardar_usuario).pack(pady=20)

    def guardar_usuario(self):
        """Guarda un nuevo usuario en la base de datos."""
        nombre = self.nombre_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        rol = self.rol_var.get()

        if not nombre or not contrasena or not rol:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol, activo) VALUES (?, ?, ?, 1)",
                           (nombre, contrasena, rol))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' agregado con éxito.")
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")
        finally:
            conn.close()


class EditarUsuario(ctk.CTkToplevel):
    def __init__(self, master=None, usuario_id=None):
        super().__init__(master)
        self.title("Editar Usuario")
        self.geometry("400x400")
        self.usuario_id = usuario_id

        # Marco desplazable
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=380, height=380)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar datos del usuario
        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, contrasena, rol, activo FROM usuarios WHERE id = ?", (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()

        # Mostrar datos actuales en el marco desplazable
        ctk.CTkLabel(self.scrollable_frame, text=f"Editando usuario: {usuario[0]}").pack(pady=10)

        ctk.CTkLabel(self.scrollable_frame, text="Nombre de Usuario:").pack(pady=5)
        self.nombre_entry = ctk.CTkEntry(self.scrollable_frame)
        self.nombre_entry.insert(0, usuario[0])
        self.nombre_entry.pack(pady=5)

        ctk.CTkLabel(self.scrollable_frame, text="Contraseña:").pack(pady=5)
        self.contrasena_entry = ctk.CTkEntry(self.scrollable_frame, show="*")
        self.contrasena_entry.insert(0, usuario[1])
        self.contrasena_entry.pack(pady=5)

        ctk.CTkLabel(self.scrollable_frame, text="Rol:").pack(pady=5)
        self.rol_var = ctk.StringVar(value=usuario[2])
        self.rol_dropdown = ctk.CTkOptionMenu(self.scrollable_frame, variable=self.rol_var, values=["administrador", "vendedor", "almacen"])
        self.rol_dropdown.pack(pady=5)

        ctk.CTkLabel(self.scrollable_frame, text="Activo (1=Sí, 0=No):").pack(pady=5)
        self.activo_entry = ctk.CTkEntry(self.scrollable_frame)
        self.activo_entry.insert(0, usuario[3])
        self.activo_entry.pack(pady=5)

        ctk.CTkButton(self.scrollable_frame, text="Guardar", command=self.guardar_cambios).pack(pady=20)

    def guardar_cambios(self):
        """Guarda los cambios del usuario en la base de datos."""
        nuevo_nombre = self.nombre_entry.get().strip()
        nueva_contrasena = self.contrasena_entry.get().strip()
        nuevo_rol = self.rol_var.get()
        nuevo_estado = self.activo_entry.get().strip()

        if not nuevo_nombre or not nueva_contrasena or nuevo_estado not in ["0", "1"]:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y el estado debe ser 0 o 1.")
            return

        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET usuario = ?, contrasena = ?, rol = ?, activo = ?
            WHERE id = ?
        """, (nuevo_nombre, nueva_contrasena, nuevo_rol, nuevo_estado, self.usuario_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Cambios guardados con éxito.")
        self.destroy()
