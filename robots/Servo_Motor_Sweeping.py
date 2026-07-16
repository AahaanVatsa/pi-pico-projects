from servo_lib import Servo
from time import sleep

my_servo = Servo(11)

while True:
  for angle in range(0,181,1):
    my_servo.set_angle(angle)
    sleep(0.01)
  for angle in range(180,-1,-1):
    my_servo.set_angle(angle)
    sleep(0.01)