from machine import Pin, PWM
from time import sleep
import motion

motion.init()

left_ir = Pin(18, Pin.IN)
center_ir = Pin(19, Pin.IN)
right_ir = Pin(20, Pin.IN)

buzz = PWM(Pin(9, Pin.OUT))

lines_detected = 0

def tone(freq):
  buzz.duty_u16(32768)
  buzz.freq(freq)

def melody():
  for i in range(3):
    tone(400)
    sleep(0.2)
    tone(800)
    sleep(0.2)
  buzz.duty_u16(0)

sleep(2)
while True:
  while left_ir.value() == 1 and center_ir.value() == 1 and right_ir.value() == 1:
    motion.forward()
    sleep(0.2)
  while left_ir.value() == 0 and center_ir.value() == 0 and right_ir.value() == 0:
    motion.forward()
    sleep(0.2)
  lines_detected += 1
  tone(400)
  if lines_detected == 3:
    motion.stop()
    melody()
    break