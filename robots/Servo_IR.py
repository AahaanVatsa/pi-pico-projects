from machine import Pin
from servo_lib import Servo
from time import sleep

my_servo = Servo(11)

ir1 = Pin(6, Pin.IN)
ir2 = Pin(3, Pin.IN)

while True:
  if i21.value() == 0:
    my_servo.set_angle(0)
  elif ir2.value() == 0:
    my_servo.set_angle(180)
  else:
    my_servo.set_angle(90)
  sleep(0.1)