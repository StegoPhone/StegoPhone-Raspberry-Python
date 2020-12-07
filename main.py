# import the CircuitPython board and busio libraries
import board
import busio
import digitalio
import time
import serial
from sparkfun_serlcd import Sparkfun_SerLCD_UART
from QwiicTwist import Sparkfun_QwiicTwist
from QwiicKeypad import Sparkfun_QwiicKeypad
import config


# Enable UART Serial communication
ttyAMA1 = serial.Serial(
        port=config.LCD_SERIAL_PORT,
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

serLCD = Sparkfun_SerLCD_UART(ttyAMA1)
def clearLCD():
    data = bytearray()
    data.append(0xFE)
    data.append(0x01)
    serLCD._write_bytes(data)

# setup IO
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
rn52EN = digitalio.DigitalInOut(board.D24)
rn52EN.direction = digitalio.Direction.OUTPUT
rn52EN.value = False

twist = Sparkfun_QwiicTwist(i2c)  # default address is 0x3F
keypad = Sparkfun_QwiicKeypad(i2c) # default address is 0x4b

clearLCD()
serLCD.set_cursor(0,0)
serLCD.write('StegoPhone')

serLCD.set_cursor(0,1)
serLCD.write("Init twist")
twist.set_color(0xFF,0x67,0x00) # Safety Orange

serLCD.set_cursor(0,1)
serLCD.write("Init SPI  ") # spaces to clear 'twist'
twist.set_color(0xFF,0x80,0x20) # increment color

while not spi.try_lock():
    pass
spi.configure(baudrate=16000000)
spi.unlock()

serLCD.set_cursor(0,1)
serLCD.write("Init RN52 ") # spaces to clear
rn52EN.value = True

# TODO: more init

clearLCD()
serLCD.set_cursor(0,0)
serLCD.write('StegoPhone')
twist.set_color(0x00,0xFF,0xFF) # Teal

#while True:
#    spi.write(bytes(range(64)))
#    time.sleep(0.1)

