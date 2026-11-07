"""Configuración centralizada y constantes semánticas del proyecto de invernadero."""

from pathlib import Path

# Rutas de archivos
DIRECTORIO_BASE = Path(__file__).resolve().parent
DIRECTORIO_DATOS = DIRECTORIO_BASE / "datos"
RUTA_ARCHIVO_CSV = DIRECTORIO_DATOS / "temperaturas_invernadero.csv"
RUTA_GRAFICA_SALIDA = DIRECTORIO_DATOS / "grafica_temperatura.png"
RUTA_GRAFICA_HUMEDAD = DIRECTORIO_DATOS / "grafica_humedad.png"

# Esquema semántico del archivo CSV
COLUMNA_DIA_SEMANA = "dia_semana"
COLUMNA_FECHA = "fecha"
COLUMNA_HORA = "hora"
COLUMNA_TEMPERATURA = "temperatura_celsius"
COLUMNA_HUMEDAD = "humedad_porcentaje"

ENCABEZADOS_CSV = [
    COLUMNA_DIA_SEMANA,
    COLUMNA_FECHA,
    COLUMNA_HORA,
    COLUMNA_TEMPERATURA,
    COLUMNA_HUMEDAD,
]

# Diccionario de días en español
NOMBRES_DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

# Formatos de fecha y hora (formato 12 horas con AM/PM para máxima legibilidad humana)
FORMATO_FECHA = "%Y-%m-%d"
FORMATO_HORA = "%I:%M:%S %p"

# Parámetro de muestreo por defecto (parametrizable)
INTERVALO_MUESTREO_SEGUNDOS = 60
