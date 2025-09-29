#include <Wire.h>
#include <Adafruit_DRV2605.h>

//////////////////// Pines / I2C ////////////////////
#define SDA_PIN 6
#define SCL_PIN 7

Adafruit_DRV2605 drv;

//////////////////// Funciones de secuencia ////////////////////

// Modo 1: Vibración fuerte + pausa + pulso
void hapticMode1() {
  drv.setWaveform(0, 85);   // vibración fuerte
  drv.setWaveform(1, 0);    // fin
  drv.go();
  delay(300);

  drv.setWaveform(0, 47);   // pulso corto
  drv.setWaveform(1, 0);
  drv.go();
}

// Modo 2: Doble pulso rápido (notificación corta)
void hapticMode2() {
  drv.setWaveform(0, 47);   // pulso corto
  drv.setWaveform(1, 47);   // otro pulso corto
  drv.setWaveform(2, 0);
  drv.go();
}

// Modo 3: Patrón tipo alarma (fuerte → zumbido largo → fuerte)
void hapticMode3() {
  drv.setWaveform(0, 85);   // fuerte
  drv.setWaveform(1, 14);   // zumbido largo
  drv.setWaveform(2, 85);   // fuerte otra vez
  drv.setWaveform(3, 0);
  drv.go();
}

//////////////////// Setup ////////////////////
void setup() {
  Serial.begin(115200);
  delay(200);

#if defined(ARDUINO_ARCH_ESP32)
  Wire.begin(SDA_PIN, SCL_PIN);  // I2C en ESP32
#else
  Wire.begin();
#endif

  if (!drv.begin(&Wire)) {
    Serial.println("No se encontró DRV2605L en 0x5A");
    while (1) delay(10);
  }

  drv.selectLibrary(1);   // Librería de efectos
  drv.useERM();           // ERM por defecto
  drv.setMode(DRV2605_MODE_INTTRIG);

  Serial.println("Haptic listo (usa modos 1, 2, 3)...");
}

//////////////////// Loop ////////////////////
void loop() {
  Serial.println("Modo 1...");
  hapticMode1();
  delay(2000);

  Serial.println("Modo 2...");
  hapticMode2();
  delay(2000);

  Serial.println("Modo 3...");
  hapticMode3();
  delay(3000);
}
