"""Módulo para leer el archivo CSV del invernadero y generar las gráficas de temperatura y humedad."""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from configuracion import (
    COLUMNA_FECHA,
    COLUMNA_HORA,
    COLUMNA_HUMEDAD,
    COLUMNA_TEMPERATURA,
    INTERVALO_MUESTREO_SEGUNDOS,
    NOMBRES_DIAS_SEMANA,
    RUTA_ARCHIVO_CSV,
    RUTA_GRAFICA_HUMEDAD,
    RUTA_GRAFICA_SALIDA,
)

COLUMNA_FECHA_HORA = "fecha_hora"


def cargar_datos_temperatura(ruta_csv: Path = RUTA_ARCHIVO_CSV) -> pd.DataFrame:
    """Lee el archivo CSV y combina las columnas de fecha y hora en un objeto datetime ordenado."""
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV en '{ruta_csv}'.")

    datos_invernadero = pd.read_csv(ruta_csv)

    texto_fecha_hora = (
        datos_invernadero[COLUMNA_FECHA].astype(str)
        + " "
        + datos_invernadero[COLUMNA_HORA].astype(str)
    )
    datos_invernadero[COLUMNA_FECHA_HORA] = pd.to_datetime(
        texto_fecha_hora, format="%Y-%m-%d %I:%M:%S %p"
    )
    datos_invernadero = datos_invernadero.sort_values(by=COLUMNA_FECHA_HORA)

    return datos_invernadero


def calcular_tiempo_muestreo_segundos(
    tiempos: pd.Series,
    tiempo_muestreo_manual: int | None = None,
) -> int:
    """Calcula la mediana del intervalo de muestreo en segundos a partir de la serie temporal."""
    if tiempo_muestreo_manual is not None:
        return tiempo_muestreo_manual

    if len(tiempos) > 1:
        diferencias = tiempos.diff().dropna()
        return int(diferencias.median().total_seconds())

    return INTERVALO_MUESTREO_SEGUNDOS


def configurar_eje_tiempo(figura: plt.Figure, eje: plt.Axes, tiempos: pd.Series) -> None:
    """Aplica el formato de día en español, fecha y hora AM/PM sin márgenes vacíos en el eje X."""
    def formateador_eje_tiempo(valor_num: float, pos: int | None = None) -> str:
        fecha_dt = mdates.num2date(valor_num)
        dia_esp = NOMBRES_DIAS_SEMANA.get(fecha_dt.weekday(), "")
        hora_am_pm = fecha_dt.strftime("%I:%M %p")
        return f"{dia_esp}\n{fecha_dt.strftime('%d/%m')}\n{hora_am_pm}"

    eje.xaxis.set_major_formatter(plt.FuncFormatter(formateador_eje_tiempo))
    figura.autofmt_xdate(rotation=0, ha="center")
    eje.set_xlim(tiempos.min(), tiempos.max())


def crear_grafica_temperatura(
    datos_invernadero: pd.DataFrame,
    ruta_imagen_salida: Path = RUTA_GRAFICA_SALIDA,
    mostrar_en_pantalla: bool = True,
    tiempo_muestreo_segundos: int | None = None,
) -> Path:
    """Genera y guarda la gráfica lineal de temperatura (°C) del invernadero."""
    tiempos = datos_invernadero[COLUMNA_FECHA_HORA]
    temperaturas = datos_invernadero[COLUMNA_TEMPERATURA]

    tiempo_muestreo = calcular_tiempo_muestreo_segundos(tiempos, tiempo_muestreo_segundos)
    temperatura_promedio = temperaturas.mean()
    temperatura_maxima = temperaturas.max()
    temperatura_minima = temperaturas.min()

    figura, eje = plt.subplots(figsize=(11, 6), dpi=120)

    eje.plot(
        tiempos,
        temperaturas,
        label="Temperatura (°C)",
        color="#2b7bba",
        linewidth=2.2,
        marker="o",
        markersize=4,
    )

    eje.axhline(
        y=temperatura_promedio,
        color="#e66101",
        linestyle="--",
        linewidth=1.5,
        label=f"Promedio ({temperatura_promedio:.1f} °C)",
    )

    eje.fill_between(
        tiempos,
        temperaturas,
        temperatura_minima - 1.0,
        color="#2b7bba",
        alpha=0.10,
    )

    eje.set_title(
        "Monitoreo de Temperatura del Invernadero\n"
        f"[Tiempo de Muestreo: {tiempo_muestreo} s] | (Mín: {temperatura_minima:.1f} °C | Máx: {temperatura_maxima:.1f} °C)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    eje.set_xlabel("Día, Fecha y Hora de Lectura", fontsize=11)
    eje.set_ylabel("Temperatura (°C)", fontsize=11)

    configurar_eje_tiempo(figura, eje, tiempos)

    eje.grid(True, linestyle=":", alpha=0.6)
    eje.legend(loc="upper right", frameon=True)
    figura.tight_layout()

    ruta_imagen_salida.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(ruta_imagen_salida)

    if mostrar_en_pantalla:
        plt.show()

    plt.close(figura)
    return ruta_imagen_salida


def crear_grafica_humedad(
    datos_invernadero: pd.DataFrame,
    ruta_imagen_salida: Path = RUTA_GRAFICA_HUMEDAD,
    mostrar_en_pantalla: bool = True,
    tiempo_muestreo_segundos: int | None = None,
) -> Path:
    """Genera y guarda la gráfica independiente de humedad relativa (%) del invernadero."""
    if COLUMNA_HUMEDAD not in datos_invernadero.columns:
        raise KeyError(
            f"La columna '{COLUMNA_HUMEDAD}' no se encuentra en el archivo CSV."
        )

    tiempos = datos_invernadero[COLUMNA_FECHA_HORA]
    humedades = datos_invernadero[COLUMNA_HUMEDAD]

    tiempo_muestreo = calcular_tiempo_muestreo_segundos(tiempos, tiempo_muestreo_segundos)
    humedad_promedio = humedades.mean()
    humedad_maxima = humedades.max()
    humedad_minima = humedades.min()

    figura, eje = plt.subplots(figsize=(11, 6), dpi=120)

    eje.plot(
        tiempos,
        humedades,
        label="Humedad Relativa (%)",
        color="#1b9e77",
        linewidth=2.2,
        marker="s",
        markersize=4,
    )

    eje.axhline(
        y=humedad_promedio,
        color="#7570b3",
        linestyle="--",
        linewidth=1.5,
        label=f"Promedio ({humedad_promedio:.1f} %)",
    )

    eje.fill_between(
        tiempos,
        humedades,
        max(0.0, humedad_minima - 3.0),
        color="#1b9e77",
        alpha=0.12,
    )

    eje.set_title(
        "Monitoreo de Humedad Relativa del Invernadero\n"
        f"[Tiempo de Muestreo: {tiempo_muestreo} s] | (Mín: {humedad_minima:.1f} % | Máx: {humedad_maxima:.1f} %)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    eje.set_xlabel("Día, Fecha y Hora de Lectura", fontsize=11)
    eje.set_ylabel("Humedad Relativa (%)", fontsize=11)

    configurar_eje_tiempo(figura, eje, tiempos)

    eje.grid(True, linestyle=":", alpha=0.6)
    eje.legend(loc="upper right", frameon=True)
    figura.tight_layout()

    ruta_imagen_salida.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(ruta_imagen_salida)

    if mostrar_en_pantalla:
        plt.show()

    plt.close(figura)
    return ruta_imagen_salida


if __name__ == "__main__":
    tabla_invernadero = cargar_datos_temperatura()

    ruta_temp = crear_grafica_temperatura(
        datos_invernadero=tabla_invernadero,
        mostrar_en_pantalla=True,
    )
    print(f"Gráfica de temperatura guardada en: {ruta_temp}")

    if COLUMNA_HUMEDAD in tabla_invernadero.columns:
        ruta_hum = crear_grafica_humedad(
            datos_invernadero=tabla_invernadero,
            mostrar_en_pantalla=True,
        )
        print(f"Gráfica de humedad guardada en: {ruta_hum}")
