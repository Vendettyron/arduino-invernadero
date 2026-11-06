"""Módulo para leer el archivo CSV de temperaturas y generar una gráfica."""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from configuracion import (
    COLUMNA_DIA_SEMANA,
    COLUMNA_FECHA,
    COLUMNA_HORA,
    COLUMNA_TEMPERATURA,
    INTERVALO_MUESTREO_SEGUNDOS,
    NOMBRES_DIAS_SEMANA,
    RUTA_ARCHIVO_CSV,
    RUTA_GRAFICA_SALIDA,
)

COLUMNA_FECHA_HORA = "fecha_hora"

def cargar_datos_temperatura(ruta_csv: Path = RUTA_ARCHIVO_CSV) -> pd.DataFrame:
    """Lee el archivo CSV y combina las columnas de fecha y hora en un objeto datetime."""
    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en '{ruta_csv}'. "
        )

    datos_temperatura = pd.read_csv(ruta_csv)

    texto_fecha_hora = (
        datos_temperatura[COLUMNA_FECHA].astype(str)
        + " "
        + datos_temperatura[COLUMNA_HORA].astype(str)
    )
    datos_temperatura[COLUMNA_FECHA_HORA] = pd.to_datetime(
        texto_fecha_hora, format="%Y-%m-%d %I:%M:%S %p"
    )
    datos_temperatura = datos_temperatura.sort_values(by=COLUMNA_FECHA_HORA)

    return datos_temperatura


def crear_grafica_temperatura(
    datos_temperatura: pd.DataFrame,
    ruta_imagen_salida: Path = RUTA_GRAFICA_SALIDA,
    mostrar_en_pantalla: bool = True,
    tiempo_muestreo_segundos: int | None = None,
) -> Path:
    """Genera y guarda una gráfica con estadísticas del invernadero."""
    tiempos = datos_temperatura[COLUMNA_FECHA_HORA]
    temperaturas = datos_temperatura[COLUMNA_TEMPERATURA]

    # Calcular o estimar el intervalo de muestreo en segundos
    if tiempo_muestreo_segundos is None:
        if len(tiempos) > 1:
            diferencias = tiempos.diff().dropna()
            tiempo_muestreo = int(diferencias.median().total_seconds())
        else:
            tiempo_muestreo = INTERVALO_MUESTREO_SEGUNDOS
    else:
        tiempo_muestreo = tiempo_muestreo_segundos

    temperatura_promedio = temperaturas.mean()
    temperatura_maxima = temperaturas.max()
    temperatura_minima = temperaturas.min()

    figura, eje = plt.subplots(figsize=(11, 6), dpi=120)

    # Curva principal de temperatura
    eje.plot(
        tiempos,
        temperaturas,
        label="Temperatura (°C)",
        color="#2b7bba",
        linewidth=2.2,
        marker="o",
        markersize=4,
    )

    # Línea de referencia del promedio
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

    # Configuración títulos con tiempo de muestreo en segundos
    eje.set_title(
        "Monitoreo de Temperatura del Invernadero\n"
        f"[Tiempo de Muestreo: {tiempo_muestreo} s] | (Mín: {temperatura_minima:.1f} °C | Máx: {temperatura_maxima:.1f} °C)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )

      # Formato para el diseno de la grafica (Titulos, Colores, Formato de Hora etc.)
    eje.set_xlabel("Fecha y Hora de Lectura", fontsize=11)
    eje.set_ylabel("Temperatura (°C)", fontsize=11)

  
    def formateador_eje_tiempo(valor_num, pos=None):
        fecha_dt = mdates.num2date(valor_num)
        dia_esp = NOMBRES_DIAS_SEMANA.get(fecha_dt.weekday(), "")
        hora_am_pm = fecha_dt.strftime("%I:%M %p")
        return f"{dia_esp}\n{fecha_dt.strftime('%d/%m')}\n{hora_am_pm}"

    eje.xaxis.set_major_formatter(plt.FuncFormatter(formateador_eje_tiempo))
    figura.autofmt_xdate(rotation=0, ha="center")
    eje.set_xlim(tiempos.min(), tiempos.max())

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
    tabla_temperaturas = cargar_datos_temperatura()
    ruta_grafica = crear_grafica_temperatura(
        datos_temperatura=tabla_temperaturas,
        mostrar_en_pantalla=True,
    )
    print(f"Gráfica guardada exitosamente en: {ruta_grafica}")

