from imu import MPU6050
from i2c_lcd import I2cLcd
from time import sleep
from machine import Pin, I2C
import motion

i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)

imu = MPU6050(i2c, device_addr = 0x68)
lcd = I2cLcd(i2c, 0x27, 2, 16)

motion.init()

tilt_threshold = 1.0

while True:
  
  gx = round(imu.gyro.x, 2)
  gy = round(imu.gyro.y, 2)

  if gx > tilt_threshold:
    motion.forward()
    
  elif gx < -tilt_threshold:
    motion.backward()
    
  elif gy > tilt_threshold:
    motion.left()
    
  elif gy < -tilt_threshold:
    motion.right()
    
  else:
    motion.stop()

  sleep(0.15)
