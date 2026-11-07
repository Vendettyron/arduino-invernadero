# Monitoreo de Temperatura para Invernadero (Arduino + Python)

Sistema de adquisición, almacenamiento y visualización gráfica de temperaturas para invernadero.

## 📌 Arquitectura del Proyecto

1. **Arduino (`arduino-invernadero.ino`)**:
   - Lee el sensor digital de la familia DHT (`DHT22` en Wokwi / `DHT11` en hardware físico en el pin digital `2`).
   - Muestreo periódico no bloqueante mediante `millis()` según la constante `INTERVALO_ENVIO_MS`.
   - Transmite los datos por el puerto Serial (`TEMP:XX.XX`).

2. **Simulador Wokwi (`wokwi.toml` y `diagram.json`)**:
   - Simula un Arduino Uno conectado a un sensor digital `wokwi-dht22` en el pin `2`.
   - Expone el puerto serie virtual en `rfc2217://localhost:4000` para comunicarse en tiempo real con Python.

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

### 3. Simular con Wokwi y capturar en tiempo real con Python
1. Si modificas `arduino-invernadero.ino`, vuelve a compilar el firmware:
   ```bash
   arduino-cli compile --fqbn arduino:avr:uno --output-dir build/arduino.avr.uno .
   ```
2. Abre `diagram.json` en VS Code y presiona **Start Simulation** (botón Play).
3. Con la simulación corriendo, abre una terminal y ejecuta:
   ```bash
   python lector_serial.py
   ```
   Verás cómo cada lectura simulada en Wokwi se guarda en `datos/temperaturas_invernadero.csv` en vivo (puedes hacer clic sobre el sensor DHT22 en Wokwi para mover el control deslizante de temperatura y ver cómo cambia).

### 4. Capturar datos reales desde tu Arduino físico (DHT11)
1. En `arduino-invernadero.ino`, cambia `const uint8_t TIPO_SENSOR_DHT = DHT22;` a `DHT11` y súbelo a tu placa.
2. En `configuracion_serial.py`, cambia `PUERTO_SERIAL_ARDUINO` al puerto USB de tu Arduino (ej. `/dev/cu.usbmodem...` o `COM3`).
3. Ejecuta el receptor:
   ```bash
   python lector_serial.py
   ```
