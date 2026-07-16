#Import necessary modules
from machine import Pin, I2C
from imu import MPU6050
from time import sleep, ticks_ms, ticks_diff
import motion

#Initialize motors, LCD, and MPU6050 sensor
motion.init()
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c, device_addr=0x68)

#Gives time for initialization
sleep(2)

#Variables for stabilization
samples = 500
gyro_bias = 0

#Loops runs 500 times; takes z-axis readings
for i in range(samples):
  gyro_bias += imu.gyro.z
  sleep(0.002)

#Takes average of all readings
gyro_bias /= samples
sleep(1)

#Function to make car follow straight line for any duration
def move_straight_pd(duration):
  kp = 170 #Magnitude of error correction (proportional gain)
  base_speed = 35000

  current_angle = 0.0
  target_angle = 0.0

  last_time = ticks_ms()
  start_time = ticks_ms
  
  #Keeps track of time; continuously updates current time and last time
  while ticks_diff(ticks_ms, start_time) < duration * 1000:
    now = ticks_ms()
    dt_ms = ticks_diff(now, last_time) #Keeps track of all differences of time
    dt = dt_ms/1000
    last_time = now

    gz = (imu.gyro.z - gyro_bias) * 52.2958
    if abs(gz) < 0.1:
      gz = 0
    current_angle += gz * dt

    error = target_angle - current_angle
    correction = kp * error

    #Improves deviation to the right
    left_speed = int(base_speed + correction)
    right_speed = int(base_speed - correction)

    if left_speed < 0:
      left_speed = 0
    elif left_speed > 65535:
      left_speed = 65535
      
    if right_speed < 0:
      right_speed = 0
    elif right_speed > 65535:
      right_speed = 65535

    motion.M1.value(1)
    motion.M2.value(1)
    motion.SM1.duty_u16(right_speed)
    motion.SM2.duty_u16(left_speed)
    
    sleep(0.01)
    
  motion.stop()

while True:
  move_straight_pd(10)
  sleep(2)
      
    