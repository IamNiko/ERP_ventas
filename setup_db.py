import sqlite3

def crear_base_datos():
    """
    Crea y actualiza la base de datos SQLite con las tablas necesarias:
    - usuarios: Información de usuarios con roles y permisos.
    - articulos: Información de los artículos con todos los campos adicionales.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS articulos_nueva (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_barras TEXT,
        descripcion TEXT NOT NULL,
        proveedor TEXT,
        costo REAL,
        iva REAL,
        precio_final REAL,
        margen REAL
    );
    """)

    # Migrar datos desde la tabla original si existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articulos'")
    if cursor.fetchone():
        cursor.execute("""
        INSERT INTO articulos_nueva (descripcion)
        SELECT descripcion FROM articulos;
        """)
        cursor.execute("DROP TABLE articulos;")
        cursor.execute("ALTER TABLE articulos_nueva RENAME TO articulos;")
    else:
        cursor.execute("ALTER TABLE articulos_nueva RENAME TO articulos;")

    # Insertar un usuario administrador inicial
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (nombre_usuario, contrasena, rol)
        VALUES ('admin', '1234', 'administrador')
    ''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Base de datos configurada con tablas actualizadas.")

    def crear_tabla_ventas():
        conn = sqlite3.connect("erp_ventas.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                articulo_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                total REAL NOT NULL,
                cliente TEXT,
                FOREIGN KEY (articulo_id) REFERENCES articulos (id)
            )
        """)
        conn.commit()
        conn.close()
        print("Tabla 'ventas' creada correctamente.")
    crear_tabla_ventas()

if __name__ == "__main__":
    crear_base_datos()
