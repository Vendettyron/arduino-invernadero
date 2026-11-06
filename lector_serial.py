"""Módulo receptor que escucha las lecturas enviadas por Arduino vía Serial y las guarda en el CSV con fecha y hora actual."""

from __future__ import annotations

import re
import sys
import time
from datetime import datetime

import serial

from configuracion import NOMBRES_DIAS_SEMANA, RUTA_ARCHIVO_CSV
from configuracion_serial import (
    PUERTO_SERIAL_ARDUINO,
    TIMEOUT_SERIAL_SEGUNDOS,
    VELOCIDAD_BAUDIOS,
)
from gestor_csv import asegurar_archivo_csv_con_encabezados, registrar_lectura_temperatura

# Expresión regular para extraer números flotantes de líneas como "TEMP:24.50" o "24.50"
PATRON_TEMPERATURA = re.compile(r"TEMP:?\s*([+-]?\d+(?:\.\d+)?)")


def extraer_temperatura(linea_texto: str) -> float | None:
    """Extrae el valor numérico de la temperatura a partir del mensaje recibido."""
    coincidencia = PATRON_TEMPERATURA.search(linea_texto)
    if coincidencia:
        return float(coincidencia.group(1))

    # Intento de parseo directo si Arduino solo envió el número
    try:
        return float(linea_texto.strip())
    except ValueError:
        return None


def iniciar_escucha_serial(
    puerto: str = PUERTO_SERIAL_ARDUINO,
    baudios: int = VELOCIDAD_BAUDIOS,
    timeout: float = TIMEOUT_SERIAL_SEGUNDOS,
) -> None:
    """Abre la conexión serial y registra cada temperatura entrante en el archivo CSV."""
    asegurar_archivo_csv_con_encabezados(RUTA_ARCHIVO_CSV)

    print(f"Conectando al puerto {puerto} a {baudios} baudios...")
    try:
        conexion = serial.Serial(port=puerto, baudrate=baudios, timeout=timeout)
    except serial.SerialException as error:
        print(f"Error al conectar con Arduino: {error}")
        print("Sugerencia: Revisa en 'configuracion_serial.py' si el nombre del puerto es el correcto.")
        sys.exit(1)

    print("Conexión serial establecida. Esperando lecturas del sensor...")
    print("Presiona Ctrl+C para detener la captura.\n")

    # Esperamos a que Arduino termine de reiniciar tras abrir el puerto
    time.sleep(2.0)

    try:
        while True:
            linea_cruda = conexion.readline().decode("utf-8", errors="ignore").strip()
            if not linea_cruda or linea_cruda.startswith("#"):
                if linea_cruda:
                    print(f"[Arduino Info]: {linea_cruda}")
                continue

            temperatura = extraer_temperatura(linea_cruda)
            if temperatura is not None:
                ahora = datetime.now()
                registrar_lectura_temperatura(
                    temperatura_celsius=temperatura,
                    momento_lectura=ahora,
                    ruta_csv=RUTA_ARCHIVO_CSV,
                )
                dia_nombre = NOMBRES_DIAS_SEMANA.get(ahora.weekday(), "")
                print(f"[{dia_nombre} {ahora.strftime('%Y-%m-%d %H:%M:%S')}] Registrado: {temperatura:.2f} °C")
            else:
                print(f"[Línea no reconocida]: {linea_cruda}")

    except KeyboardInterrupt:
        print("\nCaptura detenida por el usuario.")
    finally:
        conexion.close()
        print("Puerto serial cerrado.")


if __name__ == "__main__":
    iniciar_escucha_serial()
