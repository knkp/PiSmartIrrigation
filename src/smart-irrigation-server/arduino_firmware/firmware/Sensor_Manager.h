#pragma once
#include "Definitions.h"
#include "Arduino.h"
#include "Moisture_Sensor.h"
/*
 * Author: Stephen Copeland
 * 
 * This class is responsible for detecting, monitoring, and responding to queries about the connected sensors
 */
 

 class Sensor_Manager
 {
  public:
    Sensor_Manager(void);
    ~Sensor_Manager(void);

    String parseSerial(String input);
    void do_loop(void);
  private:
    String getValue(String input, char delim, int index);
    void setupPinMap();
    int Analog_Sensor_Count = 0;
    Moisture_Sensor* AnalogSensorList[MAX_ADC_SENSORS];
    int AnalogPinMap[MAX_ADC_SENSORS];
    unsigned long last_time_loop = -1;;
 };
