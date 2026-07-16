from machine import Pin
from time import sleep
import motion

motion.init()

rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

speed = 32768

while True:
  A = rf_A.value()
  B = rf_B.value()
  C = rf_C.value()
  D = rf_D.value()

  if A == 1:
    motion.forward(speed)
  elif B == 1:
    motion.backward(speed)
  elif C == 1:
    if speed < 65535:
      speed += 6500
  elif D == 1:
    if speed > 32768:
      speed -= 6500
  else:
    motion.stop()
  sleep(0.5)