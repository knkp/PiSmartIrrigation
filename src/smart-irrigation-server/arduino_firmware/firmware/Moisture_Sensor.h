#pragma once
#include "Arduino.h"

/*
 * Author: Stephen Copeland
 * 
 * This class is responsible for managing a moisture sensor
 */

class Moisture_Sensor
{
  public:
    // identifying marks
    int id = -1;
    String label = "";
    String sensor_type = "humidity";
    // analog pin to get data from
    int analog_pin = -1;
    float moisture_value = -1.0;
    Moisture_Sensor(void);
    ~Moisture_Sensor(void);
    
    // are we testing without sensors?
    bool mocking = false;
  
    // getters and setters
    void setPin(int pin);
    int getPin();
    void setLabel(String);
    void setSensorType(String);
    String getLabel();
    String getSensorType();
    void setId(int);
    void setMocking(bool);
    int getId();
    float returnValue();
    
    // this one's more complex, it needs to reflect the percentage value of the moisture
    float getData();
};
