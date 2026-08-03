#Import modules and functions
from machine import Pin, time_pulse_us, PWM
from time import sleep, sleep_us

#Initialize motors
motor_pin_1 = Pin(10, Pin.OUT)
motor_pin_2 = Pin(8, Pin.OUT)
enable_1 = PWM(Pin(21), freq=1000)
enable_2 = PWM(Pin(22), freq=1000)

#Declare other component Pins
buzz = PWM(Pin(9), freq=1000)
trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

#Function to convert Ultrasonic readings into distance
def get_distance():
  trig.low()
  sleep_us(2)
  trig.high()
  sleep_us(10)
  trig.low()
  duration = time_pulse_us(echo, 1)
  return int((duration * 0.0343)/2)

#Function to move robots forward and backward
def control_robot(motor_1, motor_2, motor_speed = 32768):
  enable_1.duty_u16(motor_speed)
  enable_2.duty_u16(motor_speed)
  motor_pin_1.value(m1)
  motor_pin_2.value(m2)

#Infinite loop to constantly read and display distance
while True:
  distance = get_distance()
  print("Distance: ", distance, " cm")

  #Stop or move robot
  if distance <= 15:
    control_robot(0,0,0)
  else:
    control_robot(1,1)

  #Buzzer update
  if distance > 30:
    buzz.duty_u16(0)
  elif distance > 20:
    delay = distance / 100
    buzz.duty_u16(32768)
    sleep(0.05)
    buzz.duty_u16(0)
    sleep(delay)
  else:
    buzz.duty_u16(32768)
    sleep(0.05)
    buzz.duty_u16(0)
    sleep(0.05)
  sleep(0.05)
