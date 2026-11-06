// ----------------------------------------------------------------------------
// Configuración de Pines y Parámetros
// ----------------------------------------------------------------------------
const int PIN_SENSOR_TEMPERATURA = A0;
const unsigned long INTERVALO_ENVIO_MS = 5000UL;
const float VOLTAJE_REFERENCIA = 5.0;
const float RESOLUCION_ADC = 1023.0;

unsigned long marcaTiempoUltimoEnvio = 0;

// ----------------------------------------------------------------------------
// Funciones de Lectura
// ----------------------------------------------------------------------------

float leerTemperaturaCelsius() {
  int lecturaADC = analogRead(PIN_SENSOR_TEMPERATURA);
  float voltaje = (lecturaADC * VOLTAJE_REFERENCIA) / RESOLUCION_ADC;
  
  // Fórmula para LM35:
  float temperaturaCelsius = voltaje * 100.0;
  
  return temperaturaCelsius;
}

// ----------------------------------------------------------------------------
// Configuración Inicial
// ----------------------------------------------------------------------------
void setup() {
  // Inicialización de la comunicación serial a 9600 baudios
  Serial.begin(9600);
  
  // Pequeña pausa para estabilizar la línea serial
  delay(1000);
  Serial.println(F("# Sistema de Monitoreo de Invernadero Iniciado"));
}

// ----------------------------------------------------------------------------
// Bucle Principal
// ----------------------------------------------------------------------------
void loop() {
  unsigned long tiempoActual = millis();

  // Verificamos si ha transcurrido el tiempo parametrizado
  if (tiempoActual - marcaTiempoUltimoEnvio >= INTERVALO_ENVIO_MS) {
    marcaTiempoUltimoEnvio = tiempoActual;

    float temperaturaActual = leerTemperaturaCelsius();

    Serial.print(F("TEMP:"));
    Serial.println(temperaturaActual, 2);
  }
}

