/*
 * ============================================================================
 * Proyecto: Monitoreo de Temperatura y Humedad para Invernadero
 * Sensor: Familia DHT (DHT22 en simulador Wokwi / DHT11 en hardware físico)
 * Descripción: Lee la temperatura y humedad periódicamente de forma no
 *              bloqueante y muestra el registro semántico en el Monitor Serial.
 * ============================================================================
 */

#include <DHT.h>

// ----------------------------------------------------------------------------
// Configuración Semántica del Sensor y Pines
// ----------------------------------------------------------------------------
const uint8_t PIN_SENSOR_DHT = 2; // Pin digital conectado al pin DATA/SDA del DHT

// En el simulador Wokwi se usa DHT22.
// Cuando conectes tu sensor físico DHT11, solo cambia DHT22 por DHT11 aquí:
const uint8_t TIPO_SENSOR_DHT = DHT22;

// Intervalo parametrizable de muestreo en milisegundos (ejemplo: 5000 ms = 5 s)
const unsigned long INTERVALO_ENVIO_MS = 5000UL;

// Velocidad de comunicación serial
const unsigned long VELOCIDAD_SERIAL_BAUDIOS = 9600UL;

// Día de la semana parametrizable para el registro en Arduino
const char* DIA_SEMANA_ACTUAL = "Sabado";

// ----------------------------------------------------------------------------
// Estructura Semántica de Lectura Ambiental
// ----------------------------------------------------------------------------
struct LecturaAmbiental {
  float temperaturaCelsius;
  float humedadPorcentaje;
  bool lecturaValida;
};

// ----------------------------------------------------------------------------
// Instancia del Sensor y Reloj Interno Basado en Hora de Compilación
// ----------------------------------------------------------------------------
DHT sensorInvernadero(PIN_SENSOR_DHT, TIPO_SENSOR_DHT);
unsigned long marcaTiempoUltimoEnvio = 0;
unsigned long segundosInicialesDelDia = 0;

/**
 * Convierte la macro __TIME__ ("HH:MM:SS") del compilador a segundos del día
 * para que Arduino lleve la hora real en formato AM/PM sin requerir módulo RTC.
 */
unsigned long obtenerSegundosDesdeHoraCompilacion() {
  int horas = (__TIME__[0] - '0') * 10 + (__TIME__[1] - '0');
  int minutos = (__TIME__[3] - '0') * 10 + (__TIME__[4] - '0');
  int segundos = (__TIME__[6] - '0') * 10 + (__TIME__[7] - '0');
  return (horas * 3600UL) + (minutos * 60UL) + segundos;
}

/**
 * Formatea la hora actual (calculada con millis) en formato 12 horas (HH:MM:SS AM/PM).
 */
void formatearHoraAmPm(char* bufferSalida, size_t tamanoBuffer) {
  unsigned long segundosTotales = (segundosInicialesDelDia + (millis() / 1000UL)) % 86400UL;
  uint8_t horas24 = segundosTotales / 3600UL;
  uint8_t minutos = (segundosTotales % 3600UL) / 60UL;
  uint8_t segundos = segundosTotales % 60UL;

  const char* periodo = (horas24 >= 12) ? "PM" : "AM";
  uint8_t horas12 = horas24 % 12;
  if (horas12 == 0) {
    horas12 = 12;
  }

  snprintf(bufferSalida, tamanoBuffer, "%02u:%02u:%02u %s", horas12, minutos, segundos, periodo);
}

// ----------------------------------------------------------------------------
// Funciones Semánticas de Lectura y Envío
// ----------------------------------------------------------------------------

/**
 * Solicita temperatura (°C) y humedad relativa (%) al sensor DHT.
 */
LecturaAmbiental leerCondicionesInvernadero() {
  LecturaAmbiental lectura;
  lectura.temperaturaCelsius = sensorInvernadero.readTemperature();
  lectura.humedadPorcentaje = sensorInvernadero.readHumidity();
  lectura.lecturaValida = !isnan(lectura.temperaturaCelsius) && !isnan(lectura.humedadPorcentaje);
  return lectura;
}

/**
 * Imprime el mensaje personalizado en el Monitor Serial de Wokwi / Arduino.
 * Ejemplo:
 * "La temperatura el dia Sabado a las 10:28:05 AM es de 24.50 °C y la humedad esta en: 65.00 %"
 */
void enviarLecturaPorSerial(const LecturaAmbiental &lectura) {
  if (!lectura.lecturaValida) {
    Serial.println(F("# Error: No se pudo leer el sensor DHT"));
    return;
  }

  char horaFormateada[16];
  formatearHoraAmPm(horaFormateada, sizeof(horaFormateada));

  Serial.print(F("La temperatura el dia "));
  Serial.print(DIA_SEMANA_ACTUAL);
  Serial.print(F(" a las "));
  Serial.print(horaFormateada);
  Serial.print(F(" es de "));
  Serial.print(lectura.temperaturaCelsius, 2);
  Serial.print(F(" C y la humedad esta en: "));
  Serial.print(lectura.humedadPorcentaje, 2);
  Serial.println(F(" %"));
}

// ----------------------------------------------------------------------------
// Configuración Inicial
// ----------------------------------------------------------------------------
void setup() {
  Serial.begin(VELOCIDAD_SERIAL_BAUDIOS);
  sensorInvernadero.begin();
  segundosInicialesDelDia = obtenerSegundosDesdeHoraCompilacion();

  // Pausa inicial de estabilización del sensor DHT
  delay(1000);

  Serial.println(F("# Sistema de Monitoreo de Invernadero (Temperatura y Humedad) Iniciado"));
}

// ----------------------------------------------------------------------------
// Bucle Principal (No bloqueante con millis)
// ----------------------------------------------------------------------------
void loop() {
  unsigned long tiempoActual = millis();

  if (tiempoActual - marcaTiempoUltimoEnvio >= INTERVALO_ENVIO_MS) {
    marcaTiempoUltimoEnvio = tiempoActual;

    LecturaAmbiental lecturaActual = leerCondicionesInvernadero();
    enviarLecturaPorSerial(lecturaActual);
  }
}
