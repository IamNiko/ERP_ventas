import sqlite3

def crear_base_datos():
    """
    Crea una base de datos SQLite con la tabla "usuarios" que almacena
    la siguiente información:
        - id: Identificador único para cada usuario.
        - nombre_usuario: Nombre de usuario.
        - contrasena: Contraseña del usuario.
        - rol: Rol del usuario (administrador, vendedor, almacen).
        - activo: Bandera para indicar si el usuario está activo o no.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Crear tabla usuarios con jerarquías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER DEFAULT 1
        )
    ''')

    # Insertar un usuario administrador inicial
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (nombre_usuario, contrasena, rol)
        VALUES ('admin', '1234', 'administrador')
    ''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Base de datos actualizada con roles y permisos.")

if __name__ == "__main__":
    crear_base_datos()
