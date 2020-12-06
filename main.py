# import the CircuitPython board and busio libraries
import board
import busio
import time
import serial
from sparkfun_serlcd import Sparkfun_SerLCD_UART
from QwiicTwist import Sparkfun_QwiicTwist
from QwiicKeypad import Sparkfun_QwiicKeypad


# Enable UART Serial communication
# SerLCD is connected to the RPi via a USB to TTL 3.3v Serial Cable:
# https://www.sparkfun.com/products/12977
# https://www.adafruit.com/product/954
#
ttyAMA1 = serial.Serial(
        port='/dev/ttyAMA1',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

serLCD = Sparkfun_SerLCD_UART(ttyAMA1)
# setup IO
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)

twist = Sparkfun_QwiicTwist(i2c)  # default address is 0x3F
keypad = Sparkfun_QwiicKeypad(i2c) # default address is 0x4b

serLCD.clear()
serLCD.set_cursor(0,0)
serLCD.write('StegoPhone')
twist.set_color(0xFF,0x67,0x00) # Safety Orange

while not spi.try_lock():
    pass
spi.configure(baudrate=16000000)
spi.unlock()

#while True:
#    spi.write(bytes(range(64)))
#    time.sleep(0.1)

