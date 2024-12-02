import sqlite3
import pandas as pd

def cargar_ventas_desde_csv(ruta_csv):
    """Carga datos de un archivo CSV e inserta en la tabla 'ventas'."""
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Leer el archivo CSV
    ventas = pd.read_csv(ruta_csv)

    # Renombrar columnas si es necesario
    ventas.rename(columns={
        'n_comprobante': 'comprobante',
        'fecha': 'fecha',
        'cliente': 'cliente',
        'codigo': 'articulo_id',
        'cantidad': 'cantidad',
        'p_unitario': 'precio_unitario',
        'iva': 'iva',
        'precio_final': 'total'
    }, inplace=True)

    # Insertar datos en la tabla
    for index, row in ventas.iterrows():
        cursor.execute("""
            INSERT INTO ventas (fecha, articulo_id, cantidad, precio_unitario, total, cliente)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['fecha'],
            row['articulo_id'],
            row['cantidad'],
            row['precio_unitario'],
            row['total'],
            row['cliente']
        ))

    conn.commit()
    conn.close()
    print("Datos del CSV cargados correctamente.")


import customtkinter as ctk
from tkinter import ttk
import sqlite3

import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry  # Para el selector de fechas
import sqlite3

import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Para el selector de fechas
import sqlite3

class HistoricoVentas(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico de Ventas")
        self.geometry("800x600")

        # Conexión a la base de datos
        self.conn = sqlite3.connect("erp_ventas.db")
        self.cursor = self.conn.cursor()

        # Campos de búsqueda por fecha con calendario
        ctk.CTkLabel(self, text="Fecha Inicio:").grid(row=0, column=0, padx=10, pady=10)
        self.fecha_inicio_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.fecha_inicio_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Fecha Fin:").grid(row=0, column=2, padx=10, pady=10)
        self.fecha_fin_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.fecha_fin_entry.grid(row=0, column=3, padx=10, pady=10)

        # Botón para buscar
        self.buscar_button = ctk.CTkButton(self, text="Buscar", command=self.buscar_ventas)
        self.buscar_button.grid(row=0, column=4, padx=10, pady=10)

        # Vincular Enter al método buscar
        self.bind("<Return>", lambda event: self.buscar_ventas())

        # Tabla para mostrar los resultados
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.tabla = ttk.Treeview(self.tabla_frame, columns=("Fecha", "Cliente", "Artículo", "Cantidad", "Total"), show="headings")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Artículo", text="Artículo")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Total", text="Total")
        self.tabla.pack(fill="both", expand=True)

        # Configurar scrollbars
        scrollbar_y = ttk.Scrollbar(self.tabla_frame, orient="vertical", command=self.tabla.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar_y.set)

    def buscar_ventas(self):
        """Busca las ventas dentro del rango de fechas especificado."""
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()

        # Validar fechas
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Por favor, ingrese ambas fechas.")
            return

        try:
            # Limpiar la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Consultar las ventas
            self.cursor.execute("""
                SELECT fecha, cliente, articulo_id, cantidad, total
                FROM ventas
                WHERE fecha BETWEEN ? AND ?
            """, (fecha_inicio, fecha_fin))
            resultados = self.cursor.fetchall()

            # Mostrar los resultados
            for row in resultados:
                self.tabla.insert("", "end", values=row)

            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron ventas en el rango especificado.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al buscar las ventas: {e}")

    def __del__(self):
        """Cerrar la conexión a la base de datos."""
        self.conn.close()
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

class BuscadorVentas(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)

        # Crear marco para la búsqueda y tabla
        self.buscador_frame = ctk.CTkFrame(self, width=300)
        self.buscador_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.resultados_frame = ctk.CTkFrame(self)
        self.resultados_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Campos de búsqueda por fecha
        ctk.CTkLabel(self.buscador_frame, text="Fecha Inicio:").pack(pady=5)
        self.fecha_inicio_entry = DateEntry(self.buscador_frame, date_pattern="yyyy-mm-dd")
        self.fecha_inicio_entry.pack(pady=5)

        ctk.CTkLabel(self.buscador_frame, text="Fecha Fin:").pack(pady=5)
        self.fecha_fin_entry = DateEntry(self.buscador_frame, date_pattern="yyyy-mm-dd")
        self.fecha_fin_entry.pack(pady=5)

        # Botón para buscar
        self.buscar_button = ctk.CTkButton(self.buscador_frame, text="Buscar", command=self.buscar_ventas)
        self.buscar_button.pack(pady=20)

        # Vincular Enter al método buscar
        self.master.bind("<Return>", lambda event: self.buscar_ventas())

        # Tabla para mostrar los resultados
        self.tabla = ttk.Treeview(self.resultados_frame, columns=("Fecha", "Cliente", "Artículo", "Cantidad", "Total"), show="headings")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Artículo", text="Artículo")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Total", text="Total")
        self.tabla.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(self.resultados_frame, orient="vertical", command=self.tabla.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar_y.set)

    def buscar_ventas(self):
        """Buscar ventas en la base de datos según el rango de fechas."""
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()

        # Validar fechas
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Por favor, ingrese ambas fechas.")
            return

        try:
            # Limpiar la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Consultar las ventas
            conn = sqlite3.connect("erp_ventas.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, cliente, articulo_id, cantidad, total
                FROM ventas
                WHERE fecha BETWEEN ? AND ?
            """, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()

            # Mostrar los resultados
            for row in resultados:
                self.tabla.insert("", "end", values=row)

            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron ventas en el rango especificado.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al buscar las ventas: {e}")

    def __del__(self):
        """Cerrar la conexión a la base de datos."""
        self.conn.close()




if __name__ == "__main__":
    # Cargar datos desde el CSV
    ruta_csv = "db/df_limpio.csv"  # Cambia por la ruta de tu CSV
    cargar_ventas_desde_csv(ruta_csv)

    # Mostrar las ventas cargadas
    mostrar_ventas()
