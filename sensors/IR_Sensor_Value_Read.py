from machine import Pin, I2C
from time import sleep
from i2c_lcd import I2cLcd

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

ir1 = Pin(6, Pin.IN)
ir2 = Pin(3, Pin.IN)

while True:
  state_ir1 = ir1.value()
  state_ir2 = ir2.value()
  
  print("IR2: ", str(state_ir2))
