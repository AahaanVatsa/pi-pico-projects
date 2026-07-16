from machine import Pin, PWM
from time import sleep

i21 = Pin(6, Pin.IN)
ir2 = Pin(3, Pin.IN)

m1p = Pin(10,Pin.OUT)
m1n = Pin(9,Pin.OUT)
m1s = PWM(Pin(21),freq=1000)

m2p = Pin(8,Pin.OUT)
m2n = Pin(7,Pin.OUT)
m2s = PWM(Pin(22),freq=1000)

m1s.duty_u16(32768)
m2s.duty_u16(32768)

while True:
  state_ir1 = ir1.value()
  state_ir2 = ir2.value()
  if state_ir1 == 0 or state_ir2 == 0:
    m1p.value(0)
    m2p.value(0)
  else:
    m1p.value(1)
    m2p.value(1)
  sleep(0.5)