import sqlite3

def agregar_usuario(nombre_usuario, contrasena, rol):
    """
    Agrega un usuario a la base de datos de ERP de Ventas.

    Args:
        nombre_usuario (str): El nombre de usuario.
        contrasena (str): La contraseña del usuario.
        rol (str): El rol del usuario (administrador, vendedor, almacen).

    Raises:
        sqlite3.IntegrityError: Si el usuario ya existe.
    """
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    try:
        # Insertar el usuario en la tabla usuarios
        cursor.execute('''
            INSERT INTO usuarios (nombre_usuario, contrasena, rol)
            VALUES (?, ?, ?)
        ''', (nombre_usuario, contrasena, rol))
        conn.commit()
        print(f"Usuario '{nombre_usuario}' agregado con éxito.")
    except sqlite3.IntegrityError:
        # Mostrar un mensaje de error si el usuario ya existe
        print(f"Error: El usuario '{nombre_usuario}' ya existe.")
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

# Agregar un usuario
if __name__ == "__main__":
    nombre_usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")
    rol = input("Rol (administrador, vendedor, almacen): ")

    agregar_usuario(nombre_usuario, contrasena, rol)
