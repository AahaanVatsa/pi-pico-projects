from machine import Pin
from time import sleep
import ultrasonic
from servo_lib import Servo

servo_motor = Servo(11)

ultrasonic.init()

rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)

speed = 32768

angle = 90
servo_motor.set_angle(angle)

sleep(0.75)

while True:
  A = rf_A.value()
  B = rf_B.value()
  distance = ultrasonic.get_distance()
  servo_motor.set_angle(angle)
  print("Distance: ", distance, " cm", " | Servo Angle: ", angle)
  if A == 1:
    if angle > 0:
      angle -= 10
  if B == 1:
    if angle < 180:
      angle += 10
  sleep(0.5)