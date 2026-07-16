from machine import Pin, time_pulse_us, PWM
from time import sleep, sleep_us
from servo_lib import Servo

my_servo = Servo(11)

in1 = Pin(10, Pin.OUT)
in2 = Pin(9, Pin.OUT)
en1 = PWM(Pin(21), freq=1000)

in3 = Pin(8, Pin.OUT)
in4 = Pin(7, Pin.OUT)
en2 = PWM(Pin(22), freq=1000)

trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

def get_distance():
  trig.low()
  sleep_us(2)
  trig.high()
  sleep_us(10)
  trig.low()
  duration = time_pulse_us(echo, 1)
  return int((duration * 0.0343)/2)

def control_robot(in1, in2, in3, in4, speed = 32768):
  en1.duty_u16(speed)
  en2.duty_u16(speed)
  in1.value(in1)
  in2.value(in2)
  in3.value(in3)
  in4.value(in4)

while True:
  my_servo.set_angle(90)
  front = get_distance()

  if front < 20:
    control_robot(0,0,0,0,0)
    sleep(1)
    myServo.set_angle(0)
    sleep(0.5)
    right = get_distance()
    my_servo.set_angle(180)
    sleep(0.5)
    left = get_distance()
    if (left<right):
      control_robot(0,1,1,0)
      sleep(0.1)
    else:
      control_robot(1,0,0,1)
      sleep(0.1)
    sleep(0.5)
