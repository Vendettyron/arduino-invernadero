# Monitoreo de Temperatura para Invernadero (Arduino + Python)

Sistema de adquisición, almacenamiento y visualización gráfica de temperaturas para invernadero.

## 📌 Arquitectura del Proyecto

1. **Arduino (`arduino_invernadero.ino`)**:
   - Lee el sensor analógico (LM35/TMP36 en el pin `A0`).
   - Muestreo periódico no bloqueante mediante `millis()` según la constante `INTERVALO_ENVIO_MS`.
   - Transmite los datos por el puerto Serial (`TEMP:XX.XX`).

2. **Receptor Serial (`lector_serial.py`)**:
   - Escucha las lecturas entrantes por Serial USB.
   - Añade automáticamente el **día de la semana** (`Lunes`, `Martes`, etc.), la **fecha** y la **hora** exacta del sistema.
   - Almacena cada registro en el archivo CSV.

3. **Gestor de Datos (`gestor_csv.py`)**:
   - Inicializa el archivo CSV con encabezados semánticos si no existe.
   - Provee la función `registrar_lectura_temperatura()` para almacenar cada dato real proveniente de Arduino.

4. **Visualizador Gráfico (`graficador_temperatura.py`)**:
   - Carga el CSV con `pandas`.
   - Genera una gráfica con curva de temperatura, línea de promedio, valores mínimos/máximos y formato temporal en el eje X (días en español y horas AM/PM).
   - Guarda la imagen en `datos/grafica_temperatura.png`.

---

## 📋 Formato del CSV (`datos/temperaturas_invernadero.csv`)

| Columna | Descripción | Formato de Ejemplo |
| :--- | :--- | :--- |
| `dia_semana` | Día de la semana en español | `Sábado` |
| `fecha` | Fecha estándar ISO 8601 | `2026-11-07` |
| `hora` | Hora 12h con AM/PM | `12:30:00 PM` |
| `temperatura_celsius` | Valor numérico en °C (2 decimales) | `28.47` |

---

## 🚀 Puesta en Marcha

### 1. Activar el entorno virtual
```bash
source .venv/bin/activate
```

### 2. Visualizar la gráfica
```bash
python graficador_temperatura.py
```

### 3. Capturar datos reales desde Arduino
1. Conecta tu Arduino por USB.
2. Abre `configuracion_serial.py` y verifica el nombre del puerto (ej. `/dev/cu.usbmodem...` o `COM3`).
3. Ejecuta el receptor:
```bash
python lector_serial.py
```
