# StegoPhone Raspberry (Pi) Python

This repo was specifically working towards activating an RN52 on a Raspberry Pi along with some of the other I2C display equipment I had on hand. I intended to use GNURadio in the middle section. This repo is likely not going to progress.

- Raspberry Pi 4
- dtoverlay=uart3
- dtoverlay=uart5,ctsrts
- RN-52 Bluetooth on ttyAMA2 (https://www.sparkfun.com/products/12849)
- Serial LCD on ttyAMA1 (https://www.sparkfun.com/products/retired/9067)

* GPIO02 - SDA to i2c chain
* GPIO03 - SCL to i2c chain
* GPIO04 - TX to Serial LCD (uart3)
* GPIO12 - TX to RN-52 UART RX (uart5)
* GPIO13 - RX to RN-52 UART TX (uart5)
* GPIO14 - CTS to RN-52 UART CTS (uart5)
* GPIO15 - RTS to RN-52 UART RTS (uart5)
* GPIO17 - Twist INT
* GPIO18 - Keypad INT
* GPIO24 - Device Enable to RN-52 - HIGH for 1s to power on
* GPIO25 - RN-52 GPIO9 (CMD enable LOW, DATA enable HIGH. LOW at boot)

# I2C Devices

* SparkFun Qwiic Twist 0x3F
* SparkFun Qwiic Keypad 0x4B
* SparkFun Qwiic Alphanumeric Display 0x70

```
➜  StegoPhone git:(main) ✗ sudo i2cdetect -y 1
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f
40: -- -- -- -- -- -- -- -- -- -- -- 4b -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 -- -- -- -- -- -- --
```
