from machine import Pin, PWM
from time import sleep
import motion

motion.init()

left_ir = Pin(18, Pin.IN)
center_ir = Pin(19, Pin.IN)
right_ir = Pin(20, Pin.IN)

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

pos_right = 0
pos_left = 15

sleep(2)
while True:
  if center_ir.value() == 0:
    motion.forward()
    lcd.clear()
    lcd.move_to(0,0)
    lcd.print("Forward")
  elif left_ir.value() == 0:
    motion.left()
    lcd.clear()
    lcd.move_to(0,0)
    lcd.print("Left")
    lcd.move_to(pos_left, 1)
    lcd.print("<-")
    pos_left -= 1
    if pos_left < 0:
      pos_left = 15
  elif right_ir.value() == 0:
    motion.right()
    lcd.move_to(0,0)
    lcd.print("Right")
    lcd.move_to(pos_right, 1)
    lcd.print("->")
    pos_right -= 1
    if pos_left > 15:
      pos_left = 0
  else:
    motion.stop()
    