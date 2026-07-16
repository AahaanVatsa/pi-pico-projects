from imu import MPU6050
from i2c_lcd import I2cLcd
from time import sleep
from machine import Pin, I2C
import motion

i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)

imu = MPU6050(i2c, device_addr = 0x68)
lcd = I2cLcd(i2c, 0x27, 2, 16)

motion.init()

while True:
  motion.forward()
  lcd.clear()
  lcd.putstr("Moving Forward...")

  ax = round(imu.accel.x, 2)
  ay = round(imu.accel.y, 2)

  if (-1.25 < ax > 1.25) or (-1.25 < ay > 1.25):
    motion.stop()
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Accident")
    lcd.move_to(3,1)
    lcd.putstr("Detected!!")
    break

  sleep(0.15)