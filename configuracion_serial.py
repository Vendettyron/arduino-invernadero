"""Configuración de comunicación Serial (compatible con Wokwi y Arduino físico)."""

# Para usar con el simulador Wokwi en VS Code (gracias a rfc2217ServerPort = 4000 en wokwi.toml):
PUERTO_SERIAL_ARDUINO = "rfc2217://localhost:4000"

# Cuando conectes tu Arduino físico por USB, comenta la línea de arriba y descomenta la tuya:
# PUERTO_SERIAL_ARDUINO = "/dev/cu.usbmodem1101"  # Ejemplo en macOS
# PUERTO_SERIAL_ARDUINO = "COM3"                  # Ejemplo en Windows

VELOCIDAD_BAUDIOS = 9600
TIMEOUT_SERIAL_SEGUNDOS = 2.0
