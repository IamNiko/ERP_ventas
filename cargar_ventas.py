
import pandas as pd
import sqlite3

def cargar_ventas_desde_csv(ruta_csv):
    """Carga datos de un archivo CSV e inserta en la tabla 'ventas'."""
    conn = sqlite3.connect("erp_ventas.db")
    cursor = conn.cursor()

    # Leer el archivo CSV
    ventas = pd.read_csv(ruta_csv)

    # Asegurar que las columnas necesarias existan y asignar valores predeterminados si no están presentes
    if 'hora' not in ventas.columns:
        ventas['hora'] = '00:00:00'  # Valor por defecto

    if 'tipo_comprobante' not in ventas.columns:
        ventas['tipo_comprobante'] = 'Factura'  # Valor por defecto

    if 'medio_pago' not in ventas.columns:
        ventas['medio_pago'] = 'efectivo'  # Valor por defecto

    if 'numero_comprobante' not in ventas.columns:
        ventas['numero_comprobante'] = '00000000'  # Valor por defecto

    # Renombrar columnas para que coincidan con las de la base de datos
    ventas.rename(columns={
        'Unnamed: 0': 'id_articulo',  # Mapear Unnamed: 0 a id_articulo
        'n_comprobante': 'numero_comprobante',
        'fecha': 'fecha',
        'descripcion': 'descripcion',
        'cliente': 'cliente',
        'codigo': 'codigo',
        'cantidad': 'cantidad',
        'medio_pago': 'medio_pago',
        'p_unitario': 'precio_unitario',
        'iva': 'iva',
        'precio_final': 'precio_final'
    }, inplace=True)

    # Validar columnas requeridas
    required_columns = [
        'id_articulo', 'fecha', 'hora', 'descripcion', 'cantidad',
        'precio_unitario', 'iva', 'cliente', 'medio_pago',
        'tipo_comprobante', 'numero_comprobante'
    ]
    for col in required_columns:
        if col not in ventas.columns:
            raise ValueError(f"La columna requerida '{col}' no está presente en el archivo CSV.")

    # Insertar datos en la base de datos
    for _, row in ventas.iterrows():
        # Limpiar y convertir los datos para evitar errores de tipo
        fecha = str(row['fecha'])
        hora = str(row['hora'])
        descripcion = str(row['descripcion'])
        numero_comprobante = str(row['numero_comprobante'])
        cliente = str(row['cliente'])
        tipo_comprobante = str(row['tipo_comprobante'])
        medio_pago = str(row['medio_pago'])
        id_articulo = int(row['id_articulo'])
        cantidad = int(row['cantidad'])
        precio_unitario = float(row['precio_unitario'])
        iva = float(row['iva'])
        precio_final = float(row['cantidad'] * row['precio_unitario'] * (1 + row['iva'] / 100))
        total = precio_final  # Total igual al precio_final

        # Ejecutar la consulta SQL
        cursor.execute("""
            INSERT INTO ventas (
                fecha, hora, descripcion, medio_pago, id_articulo, cantidad,
                precio_unitario, iva, precio_final, total, tipo_comprobante,
                numero_comprobante, cliente
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fecha, hora, descripcion, medio_pago, id_articulo, cantidad,
            precio_unitario, iva, precio_final, total, tipo_comprobante,
            numero_comprobante, cliente
        ))

    conn.commit()
    conn.close()
    print("Datos del CSV cargados correctamente.")

if __name__ == "__main__":
    cargar_ventas_desde_csv("db/df_limpio.csv")
