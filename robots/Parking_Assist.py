from machine import Pin, PWM
from time import sleep
import motion

motion.init()

ir1 = Pin(18, Pin.IN)
ir2 = Pin(19, Pin.IN)
ir3 = Pin(20, Pin.IN)
left_ir =  Pin(3, Pin.IN)
right_ir = Pin(6, Pin.IN)

lines_detected = 0

while True:
  if left_ir.value() == 0 or right_ir.value() == 0:
    motion.stop()
  else:
    if lines_detected < 2:
      if ir1.value() == 0 and ir2.value() == 0 and ir3.value() == 0:
        motion.forward()
        lines_detected += 1
      else:
        motion.forward()
    else:
      motion.backward()
      sleep(0.2)
      motion.stop()