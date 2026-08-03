# Import necessary modules and functions
from imu import MPU6050
from time import sleep
from machine import Pin, I2C

# Initialize MPU6050
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)
imu = MPU6050(i2c, device_addr = 0x68)

# Constantly check lin. acc. and display values
while True:

  #Take readings for linear acceleration in three dimesions
  ax = round(imu.accel.x, 2) #Acceleration forward and back
  ay = round(imu.accel.y, 2) #Acceleration left and right
  az = round(imu.accel.z, 2) #Acceleration up and down

  #Print results on serial monitor
  print(" ")
  print("ax = ", ax, " m/s^2", "ay = ", ay, " m/s^2", "az = ", az, " m/s^2")
  sleep(0.1)
