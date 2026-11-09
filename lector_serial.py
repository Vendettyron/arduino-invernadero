"""Módulo receptor que escucha las lecturas de temperatura y humedad enviadas por el Arduino físico vía Serial y las guarda en el CSV."""

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
from gestor_csv import asegurar_archivo_csv_con_encabezados, registrar_lectura_invernadero

# Expresiones regulares para los logs
PATRON_TEMPERATURA = re.compile(r"(?:es de|TEMP:?)\s*([+-]?\d+(?:\.\d+)?)", re.IGNORECASE)
PATRON_HUMEDAD = re.compile(r"(?:humedad esta en:|humedad está en:|HUM:?)\s*([+-]?\d+(?:\.\d+)?)", re.IGNORECASE)


def extraer_datos_ambientales(linea_texto: str) -> tuple[float, float] | None:
    """Extrae la tupla (temperatura_celsius, humedad_porcentaje) a partir del mensaje serial."""
    coincidencia_temp = PATRON_TEMPERATURA.search(linea_texto)
    coincidencia_hum = PATRON_HUMEDAD.search(linea_texto)

    if coincidencia_temp and coincidencia_hum:
        return float(coincidencia_temp.group(1)), float(coincidencia_hum.group(1))

    if coincidencia_temp:
        return float(coincidencia_temp.group(1)), 0.0

    return None


def formatear_mensaje_log(
    dia_semana: str,
    hora_am_pm: str,
    temperatura_celsius: float,
    humedad_porcentaje: float,
) -> str:
    """Construye el mensaje semántico de salida para el registro en consola."""
    return (
        f"La temperatura el día {dia_semana} a las {hora_am_pm} "
        f"es de {temperatura_celsius:.2f} °C y la humedad está en: {humedad_porcentaje:.2f} %"
    )


def abrir_conexion_serial(
    puerto: str,
    baudios: int,
    timeout: float,
) -> serial.SerialBase:
    """Abre una conexión serial con el puerto USB del Arduino."""
    return serial.serial_for_url(
        url=puerto,
        baudrate=baudios,
        timeout=timeout,
    )


def iniciar_escucha_serial(
    puerto: str = PUERTO_SERIAL_ARDUINO,
    baudios: int = VELOCIDAD_BAUDIOS,
    timeout: float = TIMEOUT_SERIAL_SEGUNDOS,
) -> None:
    """Abre la conexión serial y registra cada lectura de temperatura y humedad en el archivo CSV."""
    asegurar_archivo_csv_con_encabezados(RUTA_ARCHIVO_CSV)

    print(f"Conectando a '{puerto}' ({baudios} baudios)...")
    try:
        conexion = abrir_conexion_serial(puerto=puerto, baudios=baudios, timeout=timeout)
    except serial.SerialException as error:
        print(f"\nError al conectar con Arduino: {error}")
        print("Sugerencia: Revisa en 'configuracion_serial.py' si el puerto COM / USB asignado es el correcto.")
        sys.exit(1)

    print("Conexión establecida. Esperando lecturas del sensor DHT...")
    print("Presiona Ctrl+C para detener la captura.\n")

    time.sleep(1.0)

    try:
        while True:
            linea_cruda = conexion.readline().decode("utf-8", errors="ignore").strip()
            if not linea_cruda:
                continue

            if linea_cruda.startswith("#"):
                print(f"[Info Arduino]: {linea_cruda}")
                continue

            lectura = extraer_datos_ambientales(linea_cruda)
            if lectura is not None:
                temperatura, humedad = lectura
                ahora = datetime.now()
                registrar_lectura_invernadero(
                    temperatura_celsius=temperatura,
                    humedad_porcentaje=humedad,
                    momento_lectura=ahora,
                    ruta_csv=RUTA_ARCHIVO_CSV,
                )
                dia_nombre = NOMBRES_DIAS_SEMANA.get(ahora.weekday(), "")
                hora_am_pm = ahora.strftime("%I:%M:%S %p")
                print(
                    formatear_mensaje_log(
                        dia_semana=dia_nombre,
                        hora_am_pm=hora_am_pm,
                        temperatura_celsius=temperatura,
                        humedad_porcentaje=humedad,
                    )
                )
            else:
                print(f"[Línea no reconocida]: {linea_cruda}")

    except KeyboardInterrupt:
        print("\nCaptura detenida por el usuario.")
    finally:
        conexion.close()
        print("Conexión serial cerrada.")


if __name__ == "__main__":
    iniciar_escucha_serial()
