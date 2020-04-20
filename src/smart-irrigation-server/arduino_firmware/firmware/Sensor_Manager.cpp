#include    "Sensor_Manager.h"

Sensor_Manager::Sensor_Manager(){
   setupPinMap();
};

Sensor_Manager::~Sensor_Manager(){
  
};

// setup pinmaps, for now we're just doing the Uno, maybe in the future others might want to add stronger controllers
void Sensor_Manager::setupPinMap()
{
  if (MAX_ADC_SENSORS == 6){
    // this is for the Arduino Uno
    AnalogPinMap[0] = A0;
    AnalogPinMap[1] = A1;
    AnalogPinMap[2] = A2;
    AnalogPinMap[3] = A3;
    AnalogPinMap[4] = A4;
    AnalogPinMap[5] = A5;  
  }
  
}

// main control loop, mostly responsible for handling threshold, updates, controlling stuff, etc
void Sensor_Manager::do_loop()
{
  // first loop, just set time and move on
  if(last_time_loop == -1)
  {
    last_time_loop = millis();
  } 
  else if ((millis() - last_time_loop) > 1000)
  {
    // OK it's been greater than a second since we last updated everything, so let's go ahead and do that, then update last time for the next cycle

    // update all sensor data
    for(int sensor = 0; sensor < Analog_Sensor_Count; sensor++)
    {
        AnalogSensorList[sensor]->getData();
    }

    // check all thresholds
    // TODO: we will have configurable checks and thresholds, update states in the control loop here

    // set all controls
    // TODO: (this will be where we turn on/off relays for sprinklers or something when we get them available



    last_time_loop = millis(); // it will invariably take some time to get through everything so update the time after we're done.
                               // remember, the arduino Uno is not an extremely fast processor so we have to try and limit our resource usage as much as possible 
                               // so we have to sacrifice a bit of concurrency and we'll handle that on the python side management-wise.
  }
}

// parse serial commands from the arduino manager
String Sensor_Manager::parseSerial(String input)
{
  String result;  
  String output = "";
  int str_len = input.length() + 1;
  char input_char[str_len];
  input.toCharArray(input_char, str_len);

  // get with                     1,    2,     3,       4
  // format to send: 'new sensor:<id>:<type>:<label>:<mocking>
  if(strncmp(input_char, "new sensor", 10) == 0){
    // we're adding a new sensor, check if there is room and if so, add it to the list of things to check

    // first check if we've already filled up the list
    if(Analog_Sensor_Count == MAX_ADC_SENSORS){
      result = "full";
    }
    else 
    {
      // OK we're good to go, let's get the details
      String _id = this->getValue(input, ':', 1);
      int id = _id.toInt();
      String label = this->getValue(input, ':', 2);
      String s_type = this->getValue(input, ':', 3);
      String mocking_str = this->getValue(input, ':', 4);
      bool is_mocking = false;
      int mocking_int = mocking_str.toInt();
      if(mocking_int == 0){
        is_mocking = false;
      } else {
        is_mocking = true;
      }  

      // now create the sensor, add what we know, add it to the heap so it's not lost after this method returns
      Moisture_Sensor* newSensor = new Moisture_Sensor;
      newSensor->setPin(AnalogPinMap[Analog_Sensor_Count]);
      newSensor->setLabel(label);
      newSensor->setSensorType(s_type);
      newSensor->setId(id);
      newSensor->setMocking(is_mocking);

      // finally add it to the list
      AnalogSensorList[Analog_Sensor_Count] = newSensor;

      // Last let's make sure we don't forget we're adding another, so iterate the count
      Analog_Sensor_Count++;

      result = "sensor added";
    }
  // get with                      1
  // format to send: 'sensor data:<id>
  } else if(strncmp(input_char, "sensor data", 11) == 0){
     // OK, this is slow, but once again we don't have to worry about threading so we can easily check for the correct sensor this way
     String _id = this->getValue(input, ':', 1);
     int id = _id.toInt();
     bool found = false;
     
     for(int sensor = 0; sensor < Analog_Sensor_Count; sensor++){
      if(AnalogSensorList[sensor]->getId() == id){
        found = true;
        float value = AnalogSensorList[sensor]->returnValue();
        result = String(value);
        break;
      }
     }
     if(found == false){
      result = "Not Found";
     }
  } else {
    // if nothing matches just reflect the input back
    result = input;
  }

  return result;
}

String Sensor_Manager::getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
