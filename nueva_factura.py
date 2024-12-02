import customtkinter as ctk
from tkinter import ttk
import sqlite3
from datetime import datetime

class NuevaFactura(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Nueva Factura")
        self.geometry("800x600")

        # Campos básicos de la factura
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        ctk.CTkLabel(self, text="Fecha:").grid(row=0, column=0, padx=10, pady=10)
        self.fecha_label = ctk.CTkLabel(self, text=self.fecha)
        self.fecha_label.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Cliente:").grid(row=1, column=0, padx=10, pady=10)
        self.cliente_entry = ctk.CTkEntry(self, placeholder_text="Ingrese el nombre del cliente")
        self.cliente_entry.grid(row=1, column=1, padx=10, pady=10)

        # Tabla para los artículos
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.tabla = ttk.Treeview(self.tabla_frame, columns=("Codigo", "Descripcion", "Cantidad", "Precio", "Total"), show="headings")
        self.tabla.heading("Codigo", text="Código")
        self.tabla.heading("Descripcion", text="Descripción")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio Unitario")
        self.tabla.heading("Total", text="Total")
        self.tabla.pack(fill="both", expand=True)

        # Botón para agregar artículos
        self.agregar_articulo_button = ctk.CTkButton(self, text="Agregar Artículo", command=self.agregar_articulo)
        self.agregar_articulo_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Botón para guardar la factura
        self.guardar_button = ctk.CTkButton(self, text="Guardar Factura", command=self.guardar_factura)
        self.guardar_button.grid(row=4, column=0, columnspan=2, pady=20)

    def agregar_articulo(self):
        """Función para agregar un artículo a la tabla."""
        # Aquí deberás abrir un cuadro de diálogo para seleccionar el artículo y cantidad
        print("Abrir interfaz para agregar artículo.")

    def guardar_factura(self):
        """Guardar los datos de la factura en la base de datos."""
        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()

        cliente = self.cliente_entry.get()
        if not cliente:
            ctk.messagebox.showerror("Error", "Debe ingresar el nombre del cliente.")
            return

        # Guardar los artículos de la factura (esto es solo una demostración)
        for item in self.tabla.get_children():
            codigo, descripcion, cantidad, precio, total = self.tabla.item(item, "values")
            cursor.execute("""
                INSERT INTO ventas (fecha, articulo_id, cantidad, precio_unitario, total, cliente)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.fecha, codigo, cantidad, precio, total, cliente))

        conn.commit()
        conn.close()
        ctk.messagebox.showinfo("Éxito", "Factura guardada correctamente.")
        self.destroy()
