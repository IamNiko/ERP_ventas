import sqlite3

def agregar_usuario(usuario, contrasena, rol):
    """
    Agrega un usuario a la base de datos de ERP de Ventas.

    Args:
        niko
        usuario (str): El nombre de usuario.
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
            INSERT INTO usuarios (usuario, contrasena, rol)
            VALUES (?, ?, ?)
        ''', (usuario, contrasena, rol))
        conn.commit()
        print(f"Usuario '{usuario}' agregado con éxito.")
    except sqlite3.IntegrityError:
        # Mostrar un mensaje de error si el usuario ya existe
        print(f"Error: El usuario '{usuario}' ya existe.")
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

# Agregar un usuario
if __name__ == "__main__":
    usuario = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")
    rol = input("Rol (administrador, vendedor, almacen): ")

    agregar_usuario(usuario, contrasena, rol)
