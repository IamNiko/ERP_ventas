import pandas as pd
import sqlite3

# Ruta del archivo CSV
csv_file_path = "db/articulos_limpios.csv"

def crear_tabla():
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_barras INTEGER,
            descripcion TEXT,
            precio_final REAL,
            iva REAL,
            rubro TEXT,
            stock INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def cargar_articulos():
    # Crear la tabla primero
    crear_tabla()
    
    # Conectar a la base de datos
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()
   
    # Leer el CSV especificando las columnas
    df = pd.read_csv(csv_file_path, usecols=['rubro', 'codigo', 'descripcion'])
   
    # Para cada artículo en el CSV
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO articulos (
                    codigo_barras, descripcion, precio_final,
                    iva, rubro, stock
                ) VALUES (
                    ?, ?, ?, ?, ?, ?
                )
            """, (
                int(row['codigo']),  # Código como entero
                row['descripcion'],
                0.0,  # Precio por defecto
                21.0,  # IVA por defecto
                row['rubro'],
                0  # Stock inicial
            ))
        except Exception as e:
            print(f"Error al insertar artículo: {row}, Error: {str(e)}")
            continue
            
    conn.commit()
    conn.close()
    print("Artículos cargados correctamente.")

if __name__ == "__main__":
    cargar_articulos()