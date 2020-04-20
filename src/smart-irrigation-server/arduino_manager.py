import sys, signal
from serial import Serial, SerialException
from time import sleep
from api_server import db, Sensor, SensorData

# The connection to the arduino
class ArduinoLink(object):
	def __init__(self, _Port='COM10', _Baud = 9600):
		self.Connected = False
		try:
			self.ArduinoSer = Serial(_Port, _Baud)
			self.Connected = True
		except SerialException:
			print('couldn\'t make a connection')

	def writeLine(self, line):
		if self.Connected:
			bytesStr = bytes(line + '\n', encoding='UTF-8')
			self.ArduinoSer.write(bytesStr)
		else:
			return 'not connected'

	def readLine(self):
		if self.Connected:
			return self.ArduinoSer.readline()
		else:
			return 'not connected'

class ArduinoManager(ArduinoLink):
	def __init__(self):
		ArduinoLink.__init__(self)
	
	# This adds mock sensors to the database and the arduino.
	# Basically, the arduino will manage 'mock' (or in other words fake) sensors
	# which will all return random numbers, we're doing it this way because we don't have 
	# the sensors in yet to test them. Once they're in, we can add them in dynamically without omcking them
	def makeMockSensorDb(self):
		db.drop_all()
		db.create_all()

		# Mock 5 humidity sensors
		total = 5
		count = 1
		while count <= total:
			labelStr = 'Humidity ' + str(count)
			newSensor = Sensor(label=labelStr, sensor_type='humidity')
			db.session.add(newSensor)
			count +=1 
		
		db.session.commit()


	def addSensorToDb(self, sensor, _mocking=False):
		id_str = str(sensor.sensor_id)
		type_str = sensor.sensor_type
		label = sensor.label
		mock = '0'
		if _mocking:
			mock = '1'

		new_sensor_cmd = f"new sensor:{id_str}:{type_str}:{label}:{mock}"
		self.writeLine(new_sensor_cmd)
		# wait a second
		sleep(1)
		result = self.readLine()		
		# TODO: error handling here
		if b"sensor added" in result:
			print(f"new {type} sensor added")
		elif b"full" in result:
			print(f"can't add {id_str}, arduino list full")
		else:
			print(f"undefined error when adding sensor {id_str} to arduino")

	def sensorDataUpdate(self, _mocking=True):
		# this method is complex, we will check in the db for all sensors defined
		# then query the arduino for the next value, if we find out that the sensor
		# does not exist, we will add it to the arduino list and get the value on the next run
		update_db = False
		sensors = Sensor.query.all()
		for sensor in sensors:
			print(f"getting data for sensor {sensor.sensor_id}")
			self.writeLine(f"sensor data:{sensor.sensor_id}")
			sleep(1) # wait a second, (eventually will probably push this to threading)
			result = self.readLine()

			if len(result) > 0:	
				if b"Not Found" in result:
					# the sensor doesn't exist on the arduino, we need to add it
					print(f"arduino doens't know sensor, adding new sensor {sensor.sensor_id}")
					self.addSensorToDb(sensor=sensor, _mocking=_mocking)
				else:
					measured_value = float(result)
					sd = SensorData(sensor_data=measured_value)
					sensor.sensor_data.append(sd)
					db.session.add(sensor)
					update_db = True
			else:
				print(f"Undefined error getting sensor data for id {sensor.sensor_id}")
		
		if update_db:
			db.session.commit()

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
	print("started arduino manager")
	manager = ArduinoManager()
	manager.makeMockSensorDb()
	while True:
		sleep(1)
		manager.sensorDataUpdate()
	