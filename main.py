# import the CircuitPython board and busio libraries
import board
import busio
import digitalio
import time
import serial
import threading
from sparkfun_serlcd import Sparkfun_SerLCD_UART
from QwiicTwist import Sparkfun_QwiicTwist
from QwiicKeypad import Sparkfun_QwiicKeypad
import config
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # twist
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # keypad

# Enable UART Serial communication
rn52 = serial.Serial(
	port=config.RN52_SERIAL_PORT,
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)

serLcdPort = serial.Serial(
	port=config.LCD_SERIAL_PORT,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)

# setup IO
serLCD = Sparkfun_SerLCD_UART(serLcdPort)
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
rn52ENH = digitalio.DigitalInOut(board.D24)
rn52ENH.direction = digitalio.Direction.OUTPUT
rn52ENH.value = False
rn52CMDL = digitalio.DigitalInOut(board.D25)
rn52CMDL.direction = digitalio.Direction.OUTPUT
rn52CMDL.value = False  # command mode

twist = Sparkfun_QwiicTwist(i2c)  # default address is 0x3F
keypad = Sparkfun_QwiicKeypad(i2c)  # default address is 0x4b
firstKeypadFifoRead = True

def clearLCD():
	data = bytearray()
	data.append(0xFE)
	data.append(0x01)
	serLCD._write_bytes(data)


def twistInterrupt():
	try:
		GPIO.wait_for_edge(17, GPIO.BOTH)
		twist.clear_interrupts()
		serLCD.write('!')
	except:
		serLCD.write('X')

def keypadInterrupt():
	try:
		GPIO.wait_for_edge(18, GPIO.BOTH)
		if firstKeypadFifoRead:
			keypad.update_fifo()
			firstKeypadFifoRead = False
		value = keypad.button()
		serLCD.write(str(value))
	except Exception as e:
		print(e)
		serLCD.write('X')

clearLCD()
serLCD.set_cursor(0, 0)
serLCD.write('StegoPhone')


def initTwist():
	serLCD.set_cursor(0, 1)
	serLCD.write("Init twist")
	if (not twist.connected()):
		serLCD.set_cursor(0, 1)
		serLCD.write("Twist not found")
		exit(1)

	twist.clear_interrupts()
	twist.set_color(0xFF, 0x67, 0x00)  # Safety Orange
	twistThread = threading.Thread(target=twistInterrupt)
	twistThread.start()


serLCD.set_cursor(0, 1)
serLCD.write("Init keypad")
keypadThread = threading.Thread(target=keypadInterrupt)
keypadThread.start()

serLCD.set_cursor(0, 1)
serLCD.write("Init SPI  ")  # spaces to clear 'twist'
twist.set_color(0xFF, 0xA0, 0x40)  # increment color

while not spi.try_lock():
	pass
spi.configure(baudrate=16000000)
spi.unlock()

serLCD.set_cursor(0, 1)
serLCD.write("Init RN52 ")  # spaces to clear
rn52ENH.value = True

# TODO: more init

clearLCD()
serLCD.set_cursor(0, 0)
serLCD.write('StegoPhone')
twist.set_color(0x00, 0xFF, 0xFF)  # Teal

# while True:
#    spi.write(bytes(range(64)))
#    time.sleep(0.1)
