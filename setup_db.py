import sqlite3

def crear_base_datos():
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Crear tabla articulos
    cursor.execute("DROP TABLE IF EXISTS articulos")
    cursor.execute("""
    CREATE TABLE articulos (
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

    # Crear tabla ventas
    cursor.execute("DROP TABLE IF EXISTS ventas")
    cursor.execute("""
    CREATE TABLE ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        id_articulo INTEGER NOT NULL,
        codigo_barras TEXT,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        iva REAL NOT NULL,
        precio_final REAL NOT NULL,
        total REAL NOT NULL,
        tipo_comprobante TEXT NOT NULL,
        medio_pago TEXT NOT NULL,
        cliente TEXT NOT NULL,
        numero_comprobante TEXT NOT NULL,
        FOREIGN KEY (id_articulo) REFERENCES articulos (id)
    )
    """)

    # Crear tabla usuarios
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL,
        activo INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()
    print("Base de datos configurada con tablas actualizadas.")

if __name__ == "__main__":
    crear_base_datos()
