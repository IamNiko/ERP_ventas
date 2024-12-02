import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class GestionArticulos(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.conn = sqlite3.connect("erp_ventas.db")
        self.cursor = self.conn.cursor()

        # Campo de búsqueda
        self.busqueda_frame = ctk.CTkFrame(self)
        self.busqueda_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(self.busqueda_frame, text="Buscar:").pack(side="left", padx=5)
        self.buscar_entry = ctk.CTkEntry(self.busqueda_frame, placeholder_text="Código de Barras, Descripción o Proveedor")
        self.buscar_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Asignar evento de Enter al campo de búsqueda
        self.buscar_entry.bind("<Return>", lambda event: self.buscar_articulo())

        ctk.CTkButton(self.busqueda_frame, text="Buscar", command=self.buscar_articulo).pack(side="left", padx=5)

        # Tabla de resultados
        self.resultados_frame = ctk.CTkScrollableFrame(self, width=self.winfo_width(), height=400)
        self.resultados_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.resultados_frame.update()  # Actualizar el tamaño dinámico del frame

    def buscar_articulo(self):
        """Busca artículos en la base de datos según el término ingresado."""
        termino = self.buscar_entry.get()
        if not termino:
            messagebox.showinfo("Información", "Por favor, ingresa un término para buscar.")
            return

        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        # Buscar en la base de datos
        query = """
        SELECT id, codigo_barras, descripcion, proveedor, costo, iva, precio_final, margen
        FROM articulos
        WHERE codigo_barras LIKE ? OR descripcion LIKE ? OR proveedor LIKE ?
        """
        self.cursor.execute(query, (f"%{termino}%", f"%{termino}%", f"%{termino}%"))
        resultados = self.cursor.fetchall()

        # Mostrar los resultados
        if resultados:
            headers = ["ID", "Código de Barras", "Descripción", "Proveedor", "Costo", "IVA", "Precio Final", "Margen", "Acciones"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(self.resultados_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

            for row, articulo in enumerate(resultados, start=1):
                for col, value in enumerate(articulo):
                    ctk.CTkLabel(self.resultados_frame, text=str(value)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                # Botón para editar
                ctk.CTkButton(
                    self.resultados_frame,
                    text="Editar",
                    command=lambda id=articulo[0]: self.editar_articulo(id)
                ).grid(row=row, column=len(headers) - 2, padx=5, pady=5)

                # Botón para eliminar
                ctk.CTkButton(
                    self.resultados_frame,
                    text="Eliminar",
                    command=lambda id=articulo[0]: self.eliminar_articulo(id)
                ).grid(row=row, column=len(headers) - 1, padx=5, pady=5)
        else:
            ctk.CTkLabel(self.resultados_frame, text="No se encontraron resultados.").pack(pady=20)

    def editar_articulo(self, id):
        """Abrir ventana para editar un artículo específico."""
        ventana = EditarArticulo(self, id)
        self.wait_window(ventana)
        self.buscar_articulo()  # Actualizar los resultados después de editar


class EditarArticulo(ctk.CTkToplevel):
    def __init__(self, master, articulo_id):
        super().__init__(master)
        self.master = master
        self.articulo_id = articulo_id
        self.conn = sqlite3.connect("erp_ventas.db")
        self.cursor = self.conn.cursor()
        self.title("Editar Artículo")
        self.geometry("400x400")

        # Configurar para que la ventana esté al frente y sea modal
        self.lift()
        self.grab_set()

        # Obtener datos del artículo
        self.cursor.execute("SELECT * FROM articulos WHERE id = ?", (self.articulo_id,))
        articulo = self.cursor.fetchone()

        if not articulo:
            messagebox.showerror("Error", "No se encontró el artículo.")
            self.destroy()
            return

        # Inicializar el diccionario para los campos
        self.entries = {}

        # Campos del formulario
        campos = ["Código de Barras", "Descripción", "Proveedor", "Costo", "IVA", "Precio Final", "Margen"]
        for idx, campo in enumerate(campos, start=1):
            ctk.CTkLabel(self, text=campo).grid(row=idx, column=0, padx=10, pady=10)
            self.entries[campo] = ctk.CTkEntry(self)
            self.entries[campo].grid(row=idx, column=1, padx=10, pady=10)

        # Pre-cargar valores en los campos
        self.entries["Código de Barras"].insert(0, str(articulo[1]) if articulo[1] is not None else "")
        self.entries["Descripción"].insert(0, str(articulo[2]) if articulo[2] is not None else "")
        self.entries["Proveedor"].insert(0, str(articulo[3]) if articulo[3] is not None else "")
        self.entries["Costo"].insert(0, str(articulo[4]) if articulo[4] is not None else "")
        self.entries["IVA"].insert(0, str(articulo[5]) if articulo[5] is not None else "")
        self.entries["Precio Final"].insert(0, str(articulo[6]) if articulo[6] is not None else "")
        self.entries["Margen"].insert(0, str(articulo[7]) if articulo[7] is not None else "")

        # Botón de guardar
        ctk.CTkButton(self, text="Guardar Cambios", command=self.guardar_cambios).grid(row=len(campos) + 1, columnspan=2, pady=20)

        # Guardar cambios con Enter
        self.bind("<Return>", lambda event: self.guardar_cambios())

    def guardar_cambios(self):
        """Guardar los cambios en la base de datos."""
        try:
            # Obtener los nuevos valores del formulario
            codigo_barras = self.entries["Código de Barras"].get()
            descripcion = self.entries["Descripción"].get()
            proveedor = self.entries["Proveedor"].get()
            costo = float(self.entries["Costo"].get()) if self.entries["Costo"].get().strip() else 0.0
            iva = float(self.entries["IVA"].get()) if self.entries["IVA"].get().strip() else 0.0
            precio_final = float(self.entries["Precio Final"].get()) if self.entries["Precio Final"].get().strip() else 0.0
            margen = float(self.entries["Margen"].get()) if self.entries["Margen"].get().strip() else 0.0

            # Verificar que los campos obligatorios no estén vacíos
            if not descripcion.strip():
                messagebox.showerror("Error", "La descripción no puede estar vacía.")
                return

            # Actualizar el artículo en la base de datos
            self.cursor.execute("""
                UPDATE articulos
                SET codigo_barras = ?, descripcion = ?, proveedor = ?, costo = ?, iva = ?, precio_final = ?, margen = ?
                WHERE id = ?
            """, (codigo_barras, descripcion, proveedor, costo, iva, precio_final, margen, self.articulo_id))
            self.conn.commit()

            messagebox.showinfo("Éxito", "El artículo se ha actualizado correctamente.")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos en los campos Costo, IVA, Precio Final y Margen.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el artículo: {e}")

    def __del__(self):
        """Cerrar la conexión a la base de datos."""
        self.conn.close()


