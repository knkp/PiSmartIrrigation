#include "Sensor_Manager.h"

Sensor_Manager sManager;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // check for commands/requests from the manager
  if(Serial.available()){
    String input = Serial.readStringUntil("\n"); 
    String result = sManager.parseSerial(input);
    Serial.println(result);
  }

  // delay are handled in the do_loop function to prevent things from locking up.
  // Not doing any threading directly to avoid complexities of mutex's situations so
  // to compensate, everytime do_loop runs, it won't actually try to do anything for a second
  // which should give the serial buffer plenty of time to catch new commands from the arduino_manager python script
  sManager.do_loop();
  
}
