#include <HX711_ADC.h>

HX711_ADC LoadCell(4,5); //Data, CLK
long t;
int const winSize = 5;
float window [winSize];
int bufInd = 0;
bool stable = false;
void setup() {
  // put your setup code here, to run once:
  pinMode(15, OUTPUT);
  digitalWrite(15, LOW);
  Serial.begin(9600);
  Serial.println("wait");
  LoadCell.begin();
  long stability = 2000;
  LoadCell.start(stability);
  LoadCell.setCalFactor(-10993.0);
  LoadCell.tareNoDelay();
}

bool checkStable(float buf[], int n) {
  float high = buf[0];
  float low = buf[0];
  for (int i = 0; i < n ; i++) {
    if(buf [i] > high)
      high = buf[i];
    else if (buf[i] < low)
      low = buf[i];
  }
  //Serial.println("high");
  //Serial.print(high);
  return (high-low <=1);
}
void loop() {
  LoadCell.update();
  //Serial.print(stable);
  //get smoothed value from data set + current calibration factor
  if (millis() > t + 10) {
    //Serial.print("Stable is ");
    //Serial.print(stable);
    //Serial.println();
    float i = LoadCell.getData();
    window[bufInd] = i*100;
    bufInd = (bufInd +1) % winSize;
    if (!stable){
      stable = checkStable(window, winSize);
      if (stable) {
         Serial.println();
         Serial.print(i*100);
      } 
    }
    else {
      stable = checkStable(window, winSize);
    }
    //Serial.print("\nWeight: ");
   
    //Serial.print("grams.");
    t = millis();
  }

  //receive from serial terminal
  if (Serial.available() > 0) {
    float i;
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay();
  }

  //check if last tare operation is complete
  if (LoadCell.getTareStatus() == true) {
    stable = false;
    //Serial.println("Tare complete");
  }
}
