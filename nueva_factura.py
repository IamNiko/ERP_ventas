import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class NuevaFactura(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.items_venta = []  # Lista para almacenar los items de la venta
        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame superior para la información de la factura
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=20, pady=(20,10))

        # Primera fila: Fecha, Hora y Tipo de Comprobante
        self.row1_frame = ctk.CTkFrame(self.header_frame)
        self.row1_frame.pack(fill="x", pady=5)

        # Fecha actual (no editable)
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        ctk.CTkLabel(self.row1_frame, text="Fecha:").pack(side="left", padx=5)
        self.fecha_label = ctk.CTkLabel(self.row1_frame, text=fecha_actual)
        self.fecha_label.pack(side="left", padx=20)

        # Hora actual (no editable)
        hora_actual = datetime.now().strftime("%H:%M:%S")
        ctk.CTkLabel(self.row1_frame, text="Hora:").pack(side="left", padx=5)
        self.hora_label = ctk.CTkLabel(self.row1_frame, text=hora_actual)
        self.hora_label.pack(side="left", padx=20)

        # Tipo de Comprobante
        ctk.CTkLabel(self.row1_frame, text="Tipo de Comprobante:").pack(side="left", padx=5)
        self.tipo_comprobante = ctk.CTkComboBox(
            self.row1_frame,
            values=["Factura", "Liquidación"],
            width=150
        )
        self.tipo_comprobante.pack(side="left", padx=20)

        # Segunda fila: Tipo de Cliente y Medio de Pago
        self.row2_frame = ctk.CTkFrame(self.header_frame)
        self.row2_frame.pack(fill="x", pady=5)

        # Tipo de Cliente
        ctk.CTkLabel(self.row2_frame, text="Tipo de Cliente:").pack(side="left", padx=5)
        self.tipo_cliente = ctk.CTkComboBox(
            self.row2_frame,
            values=["Consumidor Final", "Cuenta Corriente"],
            width=150
        )
        self.tipo_cliente.pack(side="left", padx=20)

        # Medio de Pago
        ctk.CTkLabel(self.row2_frame, text="Medio de Pago:").pack(side="left", padx=5)
        self.medio_pago = ctk.CTkComboBox(
            self.row2_frame,
            values=["Efectivo", "Mercado Pago", "Tarjeta"],
            width=150
        )
        self.medio_pago.pack(side="left", padx=20)

        # Frame para la tabla de items
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabla de items
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            columns=("codigo", "descripcion", "cantidad", "precio", "iva", "total"),
            show="headings",
            height=10
        )

        # Configurar columnas
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("precio", text="Precio Unit.")
        self.tabla.heading("iva", text="IVA")
        self.tabla.heading("total", text="Total")

        self.tabla.column("codigo", width=100)
        self.tabla.column("descripcion", width=250)
        self.tabla.column("cantidad", width=100)
        self.tabla.column("precio", width=100)
        self.tabla.column("iva", width=100)
        self.tabla.column("total", width=100)

        # Agregar scrollbars
        scrollbar_y = ttk.Scrollbar(self.tabla_frame, orient="vertical", command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(self.tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Empaquetar tabla y scrollbars
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

        # Frame para totales
        self.totales_frame = ctk.CTkFrame(self)
        self.totales_frame.pack(fill="x", padx=20, pady=10)

        # Subtotal
        ctk.CTkLabel(self.totales_frame, text="Subtotal:").pack(side="left", padx=5)
        self.subtotal_label = ctk.CTkLabel(self.totales_frame, text="$0.00")
        self.subtotal_label.pack(side="left", padx=20)

        # Impuestos (IVA)
        ctk.CTkLabel(self.totales_frame, text="Impuestos:").pack(side="left", padx=5)
        self.impuestos_label = ctk.CTkLabel(self.totales_frame, text="$0.00")
        self.impuestos_label.pack(side="left", padx=20)

        # Total
        ctk.CTkLabel(self.totales_frame, text="Total:").pack(side="left", padx=5)
        self.total_label = ctk.CTkLabel(self.totales_frame, text="$0.00")
        self.total_label.pack(side="left", padx=20)

        # Frame para botones
        self.botones_frame = ctk.CTkFrame(self)
        self.botones_frame.pack(fill="x", padx=20, pady=10)

        # Botón de búsqueda de artículos
        self.buscar_btn = ctk.CTkButton(self.botones_frame, text="Buscar Artículo", command=self.abrir_buscador)
        self.buscar_btn.pack(side="left", padx=5)

        # Botones Guardar y Cancelar
        self.guardar_btn = ctk.CTkButton(
            self.botones_frame, text="Guardar", command=self.guardar_venta
        )
        self.guardar_btn.pack(side="right", padx=5)

        self.cancelar_btn = ctk.CTkButton(
            self.botones_frame, text="Cancelar", command=self.cancelar_venta,
            fg_color="red", hover_color="darkred"
        )
        self.cancelar_btn.pack(side="right", padx=5)

        # Entry oculto para el código de barras
        self.codigo_entry = ctk.CTkEntry(self)
        self.codigo_entry.pack()
        self.codigo_entry.pack_forget()  # Lo ocultamos pero sigue activo

    def bind_events(self):
        """Configura los eventos del formulario"""
        # Vincular el evento Enter al entry de código
        self.codigo_entry.bind("<Return>", self.procesar_codigo)
        # Hacer focus en el entry de código
        self.codigo_entry.focus_set()

    def procesar_codigo(self, event=None):
        """Procesa el código de barras escaneado"""
        codigo = self.codigo_entry.get()
        self.codigo_entry.delete(0, 'end')  # Limpiar el entry

        # Buscar el artículo en la base de datos
        try:
            conn = sqlite3.connect("erp_ventas.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT codigo, descripcion, precio, iva_porcentaje 
                FROM articulos WHERE codigo = ?
            """, (codigo,))
            articulo = cursor.fetchone()
            conn.close()

            if articulo:
                # Agregar el artículo a la tabla
                precio = float(articulo[2])
                iva = precio * float(articulo[3]) / 100
                total = precio + iva
                
                self.tabla.insert("", "end", values=(
                    articulo[0],  # código
                    articulo[1],  # descripción
                    1,            # cantidad por defecto
                    f"${precio:.2f}",
                    f"${iva:.2f}",
                    f"${total:.2f}"
                ))
                
                # Actualizar totales
                self.actualizar_totales()
            else:
                messagebox.showwarning("Advertencia", "Artículo no encontrado")

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar el artículo: {str(e)}")

        # Devolver el focus al entry de código
        self.codigo_entry.focus_set()

    def actualizar_totales(self):
        """Actualiza los totales de la venta"""
        subtotal = 0.0
        impuestos = 0.0
        
        for item in self.tabla.get_children():
            valores = self.tabla.item(item)['values']
            precio = float(valores[3].replace('$', ''))
            iva = float(valores[4].replace('$', ''))
            cantidad = int(valores[2])
            
            subtotal += precio * cantidad
            impuestos += iva * cantidad

        total = subtotal + impuestos

        self.subtotal_label.configure(text=f"${subtotal:.2f}")
        self.impuestos_label.configure(text=f"${impuestos:.2f}")
        self.total_label.configure(text=f"${total:.2f}")

    def guardar_venta(self):
        """Guarda la venta en la base de datos"""
        if not self.tabla.get_children():
            messagebox.showwarning("Advertencia", "No hay items en la venta")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de guardar la venta?"):
            try:
                conn = sqlite3.connect("erp_ventas.db")
                cursor = conn.cursor()
                
                # Insertar encabezado de la venta
                cursor.execute("""
                    INSERT INTO ventas (
                        fecha, hora, tipo_comprobante, tipo_cliente, 
                        medio_pago, subtotal, impuestos, total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.fecha_label.cget("text"),
                    self.hora_label.cget("text"),
                    self.tipo_comprobante.get(),
                    self.tipo_cliente.get(),
                    self.medio_pago.get(),
                    float(self.subtotal_label.cget("text").replace('$', '')),
                    float(self.impuestos_label.cget("text").replace('$', '')),
                    float(self.total_label.cget("text").replace('$', ''))
                ))
                
                venta_id = cursor.lastrowid

                # Insertar items de la venta
                for item in self.tabla.get_children():
                    valores = self.tabla.item(item)['values']
                    cursor.execute("""
                        INSERT INTO ventas_items (
                            venta_id, codigo, cantidad, precio_unitario, 
                            iva, total
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        venta_id,
                        valores[0],  # código
                        valores[2],  # cantidad
                        float(valores[3].replace('$', '')),  # precio unitario
                        float(valores[4].replace('$', '')),  # iva
                        float(valores[5].replace('$', ''))   # total
                    ))

                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Venta guardada correctamente")
                self.limpiar_formulario()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la venta: {str(e)}")

    def cancelar_venta(self):
        """Cancela la venta actual"""
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar la venta?"):
            # En lugar de destruir, solo limpiamos el formulario y la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            self.actualizar_totales()
            self.limpiar_formulario()


    def limpiar_formulario(self):
        """Limpia el formulario para una nueva venta"""
        # Actualizar fecha y hora
        self.fecha_label.configure(text=datetime.now().strftime("%Y-%m-%d"))
        self.hora_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Resetear totales
        self.subtotal_label.configure(text="$0.00")
        self.impuestos_label.configure(text="$0.00")
        self.total_label.configure(text="$0.00")
        
        # Resetear combos
        self.tipo_comprobante.set("Factura")
        self.tipo_cliente.set("Consumidor Final")
        self.medio_pago.set("Efectivo")
        
        # Focus en el entry de código
        self.codigo_entry.focus_set()

    def abrir_buscador(self):
        """Abre la ventana de búsqueda de artículos"""
        buscador = BuscadorArticulos(self)
        buscador.grab_set()  # Hace la ventana modal

    def agregar_articulo_buscado(self, articulo):
        """Agrega el artículo seleccionado en el buscador a la tabla"""
        if articulo:
            codigo, descripcion, precio_str, _, rubro = articulo
            
            # Convertir el precio string a float, eliminando el símbolo "$" y espacios
            precio = float(precio_str.replace('$', '').replace(' ', ''))
            
            # Calcular IVA y total
            iva = precio * 0.21  # Asumiendo IVA del 21%
            total = precio + iva
            
            self.tabla.insert("", "end", values=(
                codigo,
                descripcion,
                1,  # cantidad por defecto
                f"${precio:.2f}",
                f"${iva:.2f}",
                f"${total:.2f}"
            ))
            
        self.actualizar_totales()

class BuscadorArticulos(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Buscar Artículo")
        self.geometry("800x600")
        self.articulo_seleccionado = None
        
        # Frame de búsqueda
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=20, pady=10)
        
        # Frame para criterios de búsqueda
        self.criterios_frame = ctk.CTkFrame(self.search_frame)
        self.criterios_frame.pack(fill="x", pady=5)
        
        # Selección del tipo de búsqueda
        ctk.CTkLabel(self.criterios_frame, text="Buscar por:").pack(side="left", padx=5)
        self.tipo_busqueda = ctk.CTkComboBox(
            self.criterios_frame,
            values=["Código de Barras", "Descripción", "Rubro"],
            command=self.cambiar_tipo_busqueda
        )
        self.tipo_busqueda.set("Descripción")  # Valor inicial
        self.tipo_busqueda.pack(side="left", padx=5)
        
        # Entry de búsqueda
        self.search_entry = ctk.CTkEntry(
            self.criterios_frame, 
            placeholder_text="Ingrese el término de búsqueda...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10)
        
        # ComboBox para rubros (inicialmente oculto)
        self.rubro_combo = ctk.CTkComboBox(
            self.criterios_frame,
            values=self.obtener_rubros(),
            width=300
        )
        
        # Botón de búsqueda
        self.search_button = ctk.CTkButton(
            self.criterios_frame, 
            text="Buscar", 
            command=self.buscar
        )
        self.search_button.pack(side="left", padx=10)
        
        # Tabla de resultados
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       fieldbackground="white")
        style.map('Treeview', 
                 background=[('selected', '#0078D7')],
                 foreground=[('selected', 'white')])
        
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            columns=("codigo", "descripcion", "precio", "stock", "rubro"),
            show="headings",
            style="Treeview"
        )
        
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("rubro", text="Rubro")
        
        self.tabla.column("codigo", width=100)
        self.tabla.column("descripcion", width=250)
        self.tabla.column("precio", width=100)
        self.tabla.column("stock", width=100)
        self.tabla.column("rubro", width=150)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(self.tabla_frame, orient="vertical", command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(self.tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)
        
        # Frame de botones
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        
        self.aceptar_btn = ctk.CTkButton(
            self.button_frame, 
            text="Agregar Seleccionado", 
            command=self.aceptar
        )
        self.aceptar_btn.pack(side="right", padx=5)
        
        self.cancelar_btn = ctk.CTkButton(
            self.button_frame, 
            text="Cancelar", 
            command=self.cancelar,
            fg_color="red", 
            hover_color="darkred"
        )
        self.cancelar_btn.pack(side="right", padx=5)

        # Bindings
        self.search_entry.bind("<Return>", lambda e: self.buscar())
        self.tabla.bind("<Double-1>", lambda e: self.aceptar())
        self.bind("<Escape>", lambda e: self.cancelar())
        
        # Dar foco inicial al entry de búsqueda
        self.search_entry.focus_set()

    def obtener_rubros(self):
        """Obtiene la lista de rubros de la base de datos"""
        try:
            conn = sqlite3.connect("erp_ventas.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT rubro 
                FROM articulos 
                WHERE rubro IS NOT NULL 
                ORDER BY rubro
            """)
            rubros = [row[0] for row in cursor.fetchall()]
            conn.close()
            return rubros if rubros else ["Sin rubros"]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener rubros: {str(e)}")
            return ["Sin rubros"]

    def cambiar_tipo_busqueda(self, _=None):
        """Cambia la interfaz según el tipo de búsqueda seleccionado"""
        tipo = self.tipo_busqueda.get()
        
        # Ocultar ambos widgets primero
        self.search_entry.pack_forget()
        self.rubro_combo.pack_forget()
        
        if tipo == "Rubro":
            self.rubro_combo.pack(side="left", padx=10)
            # Actualizar la lista de rubros
            rubros = self.obtener_rubros()
            self.rubro_combo.configure(values=rubros)
            if rubros:
                self.rubro_combo.set(rubros[0])
        else:
            self.search_entry.pack(side="left", padx=10)
            self.search_entry.focus_set()
            if tipo == "Código de Barras":
                self.search_entry.configure(placeholder_text="Escanee o ingrese el código...")
            else:  # Descripción
                self.search_entry.configure(placeholder_text="Ingrese el término a buscar...")

    def buscar(self):
        """Realiza la búsqueda según el criterio seleccionado"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        tipo = self.tipo_busqueda.get()
        try:
            conn = sqlite3.connect("erp_ventas.db")
            cursor = conn.cursor()
            
            if tipo == "Rubro":
                rubro = self.rubro_combo.get()
                cursor.execute("""
                    SELECT codigo_barras, descripcion, precio_final, stock, rubro 
                    FROM articulos 
                    WHERE rubro = ? AND rubro IS NOT NULL
                    ORDER BY descripcion
                """, (rubro,))
            elif tipo == "Código de Barras":
                codigo = self.search_entry.get()
                cursor.execute("""
                    SELECT codigo_barras, descripcion, precio_final, stock, rubro 
                    FROM articulos 
                    WHERE codigo_barras = ?
                """, (codigo,))
            else:  # Descripción
                busqueda = f"%{self.search_entry.get()}%"
                cursor.execute("""
                    SELECT codigo_barras, descripcion, precio_final, stock, rubro 
                    FROM articulos 
                    WHERE descripcion LIKE ?
                    ORDER BY descripcion
                """, (busqueda,))
            
            resultados = cursor.fetchall()
            
            for resultado in resultados:
                # Asegurarse de que hay 5 valores, incluso si algunos son None
                codigo = resultado[0] or ""
                descripcion = resultado[1] or ""
                precio = resultado[2] or 0
                stock = resultado[3] or 0
                rubro = resultado[4] or ""
                
                self.tabla.insert("", "end", values=(
                    codigo,
                    descripcion,
                    f"${float(precio):.2f}",
                    stock,
                    rubro
                ))
                
            conn.close()
            
            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron artículos con el criterio especificado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar artículos: {str(e)}")

    def aceptar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un artículo")
            return
            
        item = self.tabla.item(seleccion[0])
        self.articulo_seleccionado = item['values']
        self.parent.agregar_articulo_buscado(self.articulo_seleccionado)
        self.destroy()

    def cancelar(self):
        self.destroy()