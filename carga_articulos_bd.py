import pandas as pd
import sqlite3

# Ruta del archivo CSV
csv_file_path = "db/articulos_limpios.csv"

# Leer el archivo CSV
articulos_df = pd.read_csv(csv_file_path)

# Conectar a la base de datos SQLite
conn = sqlite3.connect("erp_ventas.db")
cursor = conn.cursor()

# Insertar los datos en la tabla 'articulos'
articulos_records = articulos_df.to_records(index=False)
cursor.executemany("""
INSERT OR IGNORE INTO articulos (rubro, codigo, descripcion)
VALUES (?, ?, ?);
""", [(row.rubro, row.codigo, row.descripcion) for row in articulos_records])

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Los datos del archivo CSV se han importado correctamente en la base de datos.")
