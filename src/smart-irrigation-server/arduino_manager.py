import sys
from serial import Serial, SerialException
from time import sleep

# The connection to the arduino
class ArduinoLink(object):
	def __init__(self, _Port='COM10', _Baud = 9600):
		self.Connected = False
		try:
			self.ArduinoSer = Serial(_Port, _Baud)
			self.Connected = True
		except SerialException:
			print('couldn\'t make a connection')

	def getLine(self):
		if self.Connected:
			return self.ArduinoSer.readline()
		else:
			return 'not connected'

if __name__ == "__main__":
	print("started arduino manager", file=sys.stdout)
	conn = ArduinoLink()
	while True:
		sleep(1)
		print(conn.getLine(), file=sys.stdout)
