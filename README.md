# Proyecto de invernadero Grupo X

Integrantes: 
- estudiante 1 
- estudiante 2

# Explicacion del Proyecto

1. **Archivo  (`arduino-invernadero.ino`)**:
   - Lee de forma periódica y no bloqueante (`millis()`) la temperatura (°C) y la humedad relativa (%) desde el sensor DHT conectado al pin digital `2`.
   - Transmite los datos por el puerto USB/Serial con fecha, hora en formato AM/PM y variables ambientales.
2. **Receptor Serial (`lector_serial.py`)**:
   - Escucha las lecturas entrantes por el puerto USB (compatible con Windows y macOS).
   - Registra cada muestra en el archivo CSV agregando el día de la semana (`Lunes`, `Martes`, etc.), fecha (`AAAA-MM-DD`) y hora (`HH:MM:SS AM/PM`).
   - Muestra el log en consola:
     `La temperatura el día X a las X es de  X °C y la humedad está en: X %`
3. **Gestor de Datos (`gestor_csv.py`)**:
   - Controla la creación del archivo `datos/temperaturas_invernadero.csv` y garantiza los encabazedos y que los datos se registren de manera consistente.
4. **Visualizador Gráfico (`graficador_temperatura.py`)**:
   - Genera dos gráficas independientes (`datos/grafica_temperatura.png` y `datos/grafica_humedad.png`).
   - Muestra días, horas AM/PM, promedios, máximos, mínimos y tiempo de muestreo en segundos.
   
5. **Diagrama de Simulación Previa (`diagram.json` y `wokwi.toml`)**:
   - Archivo de simulación virtual diseñado para el simulador Wokwi.
   - Permite modelar el circuito completo (placa Arduino Uno y sensor DHT) y realizar pruebas de software, comunicación serie y graficado antes de llevar a cabo el montaje con los componentes físicos reales.

---

# Estructura del Archivo CSV (`datos/temperaturas_invernadero.csv`)

| Columna | Descripción | Formato / Ejemplo |
| :--- | :--- | :--- |
| `dia_semana` | Día de la semana | `Lunes` |
| `fecha` | Fecha estándar ISO 8601 | `2026-11-09` |
| `hora` | Hora en formato 12 horas con AM/PM | `10:00:00 AM` |
| `temperatura_celsius` | Temperatura en grados Celsius | `24.50` |
| `humedad_porcentaje` | Humedad relativa del aire | `65.00` |

---

# Conexión Física del Hardware Sesor temperatura (DHT11 de 3 Pines)

- **Pin `S` (Señal / Datos):** Al pin digital **`2`** del Arduino.
- **Pin del medio (`+` / VCC):** Al pin **`5V`** (o **`3.3V`**) del Arduino.
- **Pin `-` (GND / Tierra):** A cualquier pin **`GND`** del Arduino.

# Guía de Instalación y Uso (Windows y macOS)

### 1. Requisitos Previos e Instalaciones Extra

#### A) En Windows:
1. **Python:** Descargar desde [python.org](https://www.python.org/downloads/) (Python 3.9 o superior).
   > ⚠️ **IMPORTANTE en Windows:** Al instalar Python, marcar la casilla **"Add python.exe to PATH"** en la primera ventana del instalador.
2. **Driver del Arduino (Solo si la PC no lo reconoce):**
   - Si es un Arduino Uno original, Windows suele instalar el driver automáticamente.
   - Si es una placa genérica/económica (chip CH340), descargar e instalar el driver **CH341SER** (búsqueda rápida: "CH340 driver Windows").
3. **Arduino IDE o Arduino CLI (Solo si se requiere volver a reprogramar la placa):**
   - Descargar Arduino IDE e instalar desde el gestor de librerías la librería **"DHT sensor library"** de Adafruit.

#### B) En macOS:
- Python 3 viene preinstalado o vía Homebrew (`brew install python`).
- La placa se detecta automáticamente sin drivers adicionales.

---

### 2. Configuración del Puerto USB (`configuracion_serial.py`)

Abre el archivo `configuracion_serial.py` y verifica el puerto asignado a tu Arduino:

- **En Windows:** Típicamente es un puerto COM (ejemplo: `COM3`, `COM4`, etc.):
  ```
  PUERTO_SERIAL_ARDUINO = "COM3"
  ```
  *(Para saber qué puerto COM es: Presionar `Tecla Windows + X` -> **Administrador de dispositivos** -> sección **Puertos (COM y LPT)**).*

- **En macOS:** Típicamente tiene la forma:
  ```
  PUERTO_SERIAL_ARDUINO = "/dev/cu.usbmodem21101"
  ```

---

# Pasos para Correr el Proyecto

#### Paso 1: Abrir la terminal / PowerShell en la carpeta del proyecto
- Abrir la terminal en el IDE de preferencia.

#### Paso 2: Crear y activar el entorno virtual
- **En Windows (PowerShell / CMD):**
  ```
  python -m venv .venv
  ```
  ```
  .venv\Scripts\activate
  ```
- **En macOS / Linux:**
  ```
  python3 -m venv .venv
  ```
  ```
  source .venv/bin/activate
  ```

#### Paso 3: Instalar las dependencias (solo la primera vez)
```
pip install -r requirements.txt
```

#### Paso 4: Iniciar la captura de datos en vivo hacia el CSV
Con el Arduino conectado por USB:
```bash
python lector_serial.py
```
Al ejecutar el archivo se veran los logs, ademas de guardarse los datos en`datos/temperaturas_invernadero.csv`.  
Para detener la captura, presionar `Ctrl + C`.

#### Paso 5: Generar y ver las gráficas
```
python graficador_temperatura.py
```
Se abrirán las ventanas con las gráficas interactivas y se guardarán automáticamente en:
- `datos/grafica_temperatura.png`
- `datos/grafica_humedad.png`

---

# ⚙️ ¿Cómo Cambiar el Tiempo de Muestreo de Temperatura?

El tiempo entre cada lectura se define dentro de `arduino-invernadero.ino` en la línea 19:
```cpp
const unsigned long INTERVALO_ENVIO_MS = 5000UL;
```

### Ejemplos de valores (en milisegundos):
- **Cada 5 segundos:** `5000UL` (ideal para pruebas y demostraciones rápidas).
- **Cada 30 minutos:** `1800000UL` (`30 * 60 * 1000 ms`, ideal para un monitoreo real de invernadero).
- **Cada 1 hora:** `3600000UL` (`60 * 60 * 1000 ms`).

### Pasos obligatorios para aplicar el cambio a la placa Arduino:
Dado que este valor corre en el chip del microcontrolador, se debe recompilar y subir el programa tras cambiar el número:

1. **Detener el lector:** Si tienes `python lector_serial.py` corriendo en la terminal, detenlo con `Ctrl + C` (para liberar el puerto USB).
2. **Recompilar y subir a la placa:**
   - **En macOS:**
     ```bash
     /opt/homebrew/bin/arduino-cli compile --fqbn arduino:avr:uno --output-dir build/arduino.avr.uno . && /opt/homebrew/bin/arduino-cli upload -p /dev/cu.usbmodem21101 --fqbn arduino:avr:uno .
     ```
   - **En Windows (usando Arduino IDE):**
     Abrir `arduino-invernadero.ino`, cambiar el valor y presionar el botón **Subir** (la flecha hacia la derecha `->`).
3. **Reiniciar la captura:** Vuelve a ejecutar `python lector_serial.py`.

---

## Glosario de Conceptos Clave (Marco Conceptual)

Definiciones breves y sencillas para comprender la tecnología utilizada en el proyecto:

- **Microcontrolador (Arduino):** Es un pequeño "cerebro" electrónico programable capaz de recibir señales de sensores del mundo real y enviar información a una computadora.
- **Sensor Digital (DHT11):** Dispositivo electrónico que mide el calor del ambiente (temperatura en °C) y la cantidad de vapor de agua en el aire (humedad relativa en %), transformándolo en pulsos binarios.
- **Puerto Serial / USB:** Canal de comunicación por cable que permite al Arduino enviar texto y números hacia la computadora de manera ordenada, un bit a la vez.
- **Baudios (Baud Rate):** Unidad que mide la velocidad de transmisión de datos por segundo. En este proyecto se usan 9600 baudios, estándar ideal para lecturas estables de sensores.
- **Archivo CSV (Comma-Separated Values):** Formato de texto plano que organiza datos en filas y columnas separadas por comas. Es universal y puede abrirse con Microsoft Excel o Bloc de notas.
- **Entorno Virtual (`.venv`):** Carpeta aislada dentro de la computadora que guarda las librerías del proyecto para no mezclar versiones ni afectar otros programas de la máquina.
- **Librería de Programación:** Paquete de código ya programado por otros desarrolladores que nos evita reinventar la rueda (por ejemplo: `pandas` para manipular tablas de datos y `matplotlib` para dibujar gráficas).
- **Muestreo No Bloqueante (`millis()`):** Técnica de programación en Arduino que mide el paso del tiempo con un cronómetro interno en lugar de pausar o "congelar" el microcontrolador (evitando el uso de `delay()`).
