#Import necessary modules
from imu import MPU6050
from time import sleep
from machine import Pin, I2C

#Initilizing components
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)
imu = MPU6050(i2c, device_addr = 0x68)

#Infinite loop to constantly read values
while True:

  #Take readings for rotation in three dimesions (Roll, Pitch, Yaw)
  gx = round(imu.gyro.x, 2) #Rotation around front-back axis
  gy = round(imu.gyro.y, 2) #Rotation around lef-right axis
  gz = round(imu.gyro.z, 2) #Rotation around up-down axis
  
  #Print results in serial monitor
  print(" ")
  print("gx = ", gx, " m/s^2", "gy = ", gy, " m/s^2", "gz = ", gz, " m/s^2")
  sleep(0.01)
