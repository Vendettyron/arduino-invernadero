"""Módulo encargado de la gestión y almacenamiento de lecturas reales de temperatura y humedad en el CSV."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from configuracion import (
    ENCABEZADOS_CSV,
    FORMATO_FECHA,
    FORMATO_HORA,
    NOMBRES_DIAS_SEMANA,
    RUTA_ARCHIVO_CSV,
)


def asegurar_archivo_csv_con_encabezados(ruta_csv: Path = RUTA_ARCHIVO_CSV) -> None:
    """Crea el directorio y el archivo CSV con sus encabezados si no existe."""
    ruta_csv.parent.mkdir(parents=True, exist_ok=True)

    archivo_existe_y_tiene_contenido = ruta_csv.exists() and ruta_csv.stat().st_size > 0
    if not archivo_existe_y_tiene_contenido:
        with ruta_csv.open(mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(ENCABEZADOS_CSV)


def registrar_lectura_invernadero(
    temperatura_celsius: float,
    humedad_porcentaje: float,
    momento_lectura: datetime | None = None,
    dia_semana_personalizado: str | None = None,
    ruta_csv: Path = RUTA_ARCHIVO_CSV,
) -> None:
    """Registra una lectura real de temperatura (°C) y humedad (%) con día, fecha y hora."""
    asegurar_archivo_csv_con_encabezados(ruta_csv)

    instante_actual = momento_lectura or datetime.now()

    dia_semana = (
        dia_semana_personalizado
        if dia_semana_personalizado
        else NOMBRES_DIAS_SEMANA.get(instante_actual.weekday(), "Desconocido")
    )
    fecha_formateada = instante_actual.strftime(FORMATO_FECHA)
    hora_formateada = instante_actual.strftime(FORMATO_HORA)
    temperatura_redondeada = f"{temperatura_celsius:.2f}"
    humedad_redondeada = f"{humedad_porcentaje:.2f}"

    fila_registro = [
        dia_semana,
        fecha_formateada,
        hora_formateada,
        temperatura_redondeada,
        humedad_redondeada,
    ]

    with ruta_csv.open(mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(fila_registro)
        archivo.flush()

registrar_lectura_temperatura = registrar_lectura_invernadero


if __name__ == "__main__":
    asegurar_archivo_csv_con_encabezados()
    print(f"Gestor CSV activo y listo para almacenar lecturas en: {RUTA_ARCHIVO_CSV}")
