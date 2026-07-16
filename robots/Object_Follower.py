from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
import motion

ir1 = Pin(6, Pin.IN)
ir2 = Pin(3, Pin.IN)

trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

motion.init()

def get_distace():
  trig.low()
  sleep_us(2)
  trig.high()
  sleep_us(10)
  trig.low()
  duration = time_pulse_us(echo,1)
  return int(duration * 0.0344/2)
sleep(1)

while True:
  dist = get_distace()
  left = ir1.value()
  right = ir2.value()
  print(left, right)
  sleep(1)
  if dist <= 3:
    motion.stop()
  elif left == 0 and right == 0:
    motion.forward()
  elif left == 0:
    motion.left()
  elif right == 0:
    motion.right()
  elif dist <= 20:
    motion.forward()
  else:
    motion.stop()
  sleep(0.05)