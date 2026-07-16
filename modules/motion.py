
from machine import Pin, PWM

M1 = None
M2 = None
SM1 = None
SM2 = None

def init():
  global M1, M2, SM1, SM2
  M1 = Pin(10,Pin.OUT)
  M2 = Pin(8,Pin.OUT)
  SM1 = PWM(Pin(21),freq=1000)
  SM2 = PWM(Pin(22),freq=1000)

def forward(speed=32768):
  SM1.duty_u16(speed)
  SM2.duty_u16(speed)
  M1.value(1)
  M2.value(1)

def backward(speed=32768):
  SM1.duty_u16(speed)
  SM2.duty_u16(speed)
  M1.value(0)
  M2.value(0)

def left(speed=32768):
  SM1.duty_u16(speed)
  SM2.duty_u16(speed)
  M1.value(1)
  M2.value(0) 

def right(speed=32768):
  SM1.duty_u16(speed)
  SM2.duty_u16(speed)
  M1.value(0)
  M2.value(1)  

def stop():
  SM1.duty_u16(0)
  SM2.duty_u16(0)

def curve_turn(left_speed, right_speed):
  SM1.duty_u16(right_speed)
  SM2.duty_u16(left_speed)
  M1.value(1)
  M2.value(1)

def swing_turn(direction, speed = 32768):
  if direction == 'left':
    SM1.duty_u16(speed)
    SM2.duty_u16(0)
    M2.value(1)
  elif direction == 'right':
    SM1.duty_u16(0)
    SM2.duty_u16(speed)
    M1.value(1)
  else:
    stop()
