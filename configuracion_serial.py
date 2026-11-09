"""Configuración de comunicación Serial con la placa Arduino física."""

# Puerto asignado al Arduino físico:
# - En macOS típicamente: "/dev/cu.usbmodem..."
# - En Windows típicamente: "COM3", "COM4", etc.
PUERTO_SERIAL_ARDUINO = "/dev/cu.usbmodem21101"

VELOCIDAD_BAUDIOS = 9600
TIMEOUT_SERIAL_SEGUNDOS = 2.0
