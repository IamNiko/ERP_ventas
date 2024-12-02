import sqlite3
import pandas as pd
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class BuscadorVentas(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        # Frame superior para los controles de búsqueda
        self.controles_frame = ctk.CTkFrame(self)
        self.controles_frame.pack(fill="x", padx=20, pady=10)

        # Título
        self.titulo = ctk.CTkLabel(self.controles_frame, text="Buscador de Ventas", 
                                 font=("Arial", 20, "bold"))
        self.titulo.pack(pady=10)

        # Frame para los campos de fecha
        self.fechas_frame = ctk.CTkFrame(self.controles_frame)
        self.fechas_frame.pack(pady=10)

        # Campos de búsqueda por fecha
        ctk.CTkLabel(self.fechas_frame, text="Fecha Inicio:").pack(side="left", padx=5)
        self.fecha_inicio_entry = DateEntry(self.fechas_frame, date_pattern="yyyy-mm-dd", width=12)
        self.fecha_inicio_entry.pack(side="left", padx=5)

        ctk.CTkLabel(self.fechas_frame, text="Fecha Fin:").pack(side="left", padx=5)
        self.fecha_fin_entry = DateEntry(self.fechas_frame, date_pattern="yyyy-mm-dd", width=12)
        self.fecha_fin_entry.pack(side="left", padx=5)

        # Botón para buscar
        self.buscar_button = ctk.CTkButton(self.fechas_frame, text="Buscar", 
                                         command=self.buscar_ventas)
        self.buscar_button.pack(side="left", padx=20)

        # Frame para la tabla
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Tabla para mostrar los resultados
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            columns=("Fecha", "Cliente", "Artículo", "Cantidad", "Total"),
            show="headings"
        )
        
        # Configurar columnas
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Artículo", text="Artículo")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Total", text="Total")
        
        # Ajustar anchos de columna
        self.tabla.column("Fecha", width=100)
        self.tabla.column("Cliente", width=200)
        self.tabla.column("Artículo", width=200)
        self.tabla.column("Cantidad", width=100)
        self.tabla.column("Total", width=100)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(self.tabla_frame, orient="vertical", 
                                  command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(self.tabla_frame, orient="horizontal", 
                                  command=self.tabla.xview)
        
        # Configurar scroll
        self.tabla.configure(yscrollcommand=scrollbar_y.set, 
                           xscrollcommand=scrollbar_x.set)
        
        # Empaquetar todo
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

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
                messagebox.showinfo("Sin resultados", 
                                  "No se encontraron ventas en el rango especificado.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al buscar las ventas: {e}")

# Opcional: función de utilidad para cargar datos de prueba
def cargar_ventas_desde_csv(ruta_csv):
    """Carga datos de un archivo CSV e inserta en la tabla 'ventas'."""
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    ventas = pd.read_csv(ruta_csv)
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