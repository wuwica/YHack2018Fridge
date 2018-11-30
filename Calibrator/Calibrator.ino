#include <HX711_ADC.h>

HX711_ADC LoadCell(4,5); //Data, CLK
long t;

void setup() {
  // put your setup code here, to run once:
  pinMode(15, OUTPUT);
  digitalWrite(15, LOW);
  Serial.begin(9600);
  Serial.println("wait");
  LoadCell.begin();
  long stability = 2000;
  LoadCell.start(stability);
  LoadCell.setCalFactor(696.0);
}

void loop() {
  LoadCell.update();

  //get smoothed value from data set + current calibration factor
  if (millis() > t + 250) {
    float i = LoadCell.getData();
    float v = LoadCell.getCalFactor();
    Serial.print("Load_cell output val: ");
    Serial.print(i);
    Serial.print("      Load_cell calFactor: ");
    Serial.println(v);
    t = millis();
  }

  //receive from serial terminal
  if (Serial.available() > 0) {
    float i;
    char inByte = Serial.read();
    if (inByte == 'l') i = -1.0;
    else if (inByte == 'L') i = -10.0;
    else if (inByte == 'h') i = 1.0;
    else if (inByte == 'H') i = 10.0;
    else if (inByte == 't') LoadCell.tareNoDelay();
    if (i != 't') {
      float v = LoadCell.getCalFactor() + i;
      LoadCell.setCalFactor(v);
    }
  }

  //check if last tare operation is complete
  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }
}
