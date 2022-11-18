#include <Servo.h>
Servo servo1;

String entradaSerial = "";         // String para almacenar entrada
bool entradaCompleta = false;  // Indicar si el String está completo

int pin = 9;    // pin de conexión PWM al servo
int pulsoMinimo = 580;  // Duración en microsegundos del pulso para girar 0º
int pulsoMaximo = 2500; // Duración en microsegundos del pulso para girar 180º
int angulo = 0; // Variable para guardar el angulo que deseamos de giro

void setup()
{
  servo1.attach(pin, pulsoMinimo, pulsoMaximo);
  Serial.begin(9600);
}

void loop()
{
  if (entradaCompleta) {
    if (entradaSerial == "izq\n") {
      if(angulo > 0)
        angulo = angulo - 1;
     //  Serial.print(angulo);
      // Giro a la izquierda
      servo1.write(angulo);
    }
    else if (entradaSerial == "izq1\n"){
      if(angulo > 0)
        angulo = angulo - 1;
      servo1.write(angulo);
    }
    else if (entradaSerial == "izq2\n"){
      if(angulo > 0)
        angulo = angulo - 1;
      servo1.write(angulo);
    }
    else if (entradaSerial == "der\n") {
      if(angulo < 180)  
        angulo = angulo + 1;
      // Serial.print(angulo);
      // Giro a la derecha
      servo1.write(angulo);
    }
    else if (entradaSerial == "der1\n"){
      if(angulo < 180)
        angulo = angulo + 1;
      servo1.write(angulo);
    }
    else if (entradaSerial == "der2\n"){
      if(angulo < 180)
        angulo = angulo + 1;
      servo1.write(angulo);
    }
    else { // Cualquier otro dato recibido
      Serial.println("El dato recibido es inválido!!");
    }
    entradaSerial = "";
    entradaCompleta = false;
  }
}

// Función que se activa al recibir algo por
// el puerto serie, Interrupción del Puerto Serie.
void serialEvent() {
  while (Serial.available()) {
    // Obtener bytes de entrada:
    char inChar = (char)Serial.read();
    // Agregar al String de entrada:
    entradaSerial += inChar;
    // Para saber si el string está completo, se detendrá al recibir
    // el caracter de retorno de línea ENTER \n
    if (inChar == '\n') {
      entradaCompleta = true;
    }
  }
}
