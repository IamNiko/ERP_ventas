import sqlite3

def crear_base_datos():
    """
    Crea y actualiza la base de datos SQLite con las tablas necesarias.
    """
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Primero vamos a guardar los datos existentes si es que hay
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articulos'")
    datos_existentes = []
    if cursor.fetchone():
        cursor.execute("SELECT * FROM articulos")
        datos_existentes = cursor.fetchall()
        # Obtener nombres de columnas existentes
        cursor.execute("PRAGMA table_info(articulos)")
        columnas_existentes = [column[1] for column in cursor.fetchall()]
        cursor.execute("DROP TABLE articulos")

    # Crear tabla usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER DEFAULT 1
        )
    ''')

    # Crear nueva tabla articulos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_barras TEXT,
        descripcion TEXT NOT NULL,
        proveedor TEXT,
        costo REAL,
        iva REAL,
        precio_final REAL,
        margen REAL,
        rubro TEXT,
        stock INTEGER DEFAULT 0
    )
    """)

    # Si había datos, los reinsertamos
    if datos_existentes:
        # Crear un mapeo entre columnas viejas y nuevas
        columnas_a_insertar = [
            "codigo_barras", "descripcion", "proveedor",
            "costo", "iva", "precio_final", "margen"
        ]
        # Agregar valores por defecto para las columnas nuevas
        valores_base = {
            "rubro": None,
            "stock": 0
        }
        
        # Insertar los datos existentes
        insert_query = f"""
            INSERT INTO articulos (
                codigo_barras, descripcion, proveedor,
                costo, iva, precio_final, margen,
                rubro, stock
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        for dato in datos_existentes:
            valores = list(dato[1:8])  # Tomamos los valores existentes (excluyendo el id)
            valores.extend([valores_base["rubro"], valores_base["stock"]])  # Agregamos los valores por defecto
            cursor.execute(insert_query, valores)

    # Insertar usuario administrador inicial
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (nombre_usuario, contrasena, rol)
        VALUES ('admin', '1234', 'administrador')
    ''')

    # Crear tabla ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            tipo_comprobante TEXT NOT NULL,
            tipo_cliente TEXT NOT NULL,
            medio_pago TEXT NOT NULL,
            subtotal REAL NOT NULL,
            impuestos REAL NOT NULL,
            total REAL NOT NULL
        )
    """)

    # Crear tabla ventas_items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Base de datos configurada con tablas actualizadas.")

if __name__ == "__main__":
    crear_base_datos()