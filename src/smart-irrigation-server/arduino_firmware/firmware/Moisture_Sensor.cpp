#include "Moisture_Sensor.h"

Moisture_Sensor::Moisture_Sensor(void)
{
  // defaults already set 
}  

void Moisture_Sensor::setPin(int pin)
{
  analog_pin = pin;
}

int Moisture_Sensor::getPin()
{
  return analog_pin;
}

void Moisture_Sensor::setLabel(String _label)
{
  label = _label;
}

String Moisture_Sensor::getLabel()
{
  return label;
}

void Moisture_Sensor::setSensorType(String _type)
{
  sensor_type = _type;
}

void Moisture_Sensor::setMocking(bool _mocking)
{
  mocking = _mocking;
}

void Moisture_Sensor::setId(int _id)
{
  id = _id;
}

int Moisture_Sensor::getId()
{
  return id;
}

float Moisture_Sensor::returnValue()
{
  return moisture_value;
}

float Moisture_Sensor::getData()
{
  if(mocking){
    // if there is no real sensor, return a random float from 1.0 to 100.0
    moisture_value = random(100,1000)/100;
    return moisture_value;
  }
  int raw_value = 0;
  if(analog_pin != -1){
    raw_value = analogRead(analog_pin);
    // return the result as a percentage from 0-100% moisture level from ADC read
    moisture_value = (100*raw_value)/1024;
  }

  // this means the pin is not set
  moisture_value = -1.0;
  return moisture_value;
  
}

String Moisture_Sensor::getSensorType()
{
  return sensor_type;
}

// destructor
Moisture_Sensor::~Moisture_Sensor(void)
{
  
}
