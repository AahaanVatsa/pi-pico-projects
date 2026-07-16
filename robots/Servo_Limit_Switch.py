from machine import Pin, I2C
from time import sleep
from servo_lib import Servo
from i2c_lcd import I2cLcd

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

my_servo = Servo(11)

next_switch = Pin(3, Pin.IN, Pin.PULL_UP)
select_switch = Pin(6, Pin.IN, Pin.PULL_UP)

angle = 0
lcd.putstr("Servo Angle Menu:")
sleep(2)
lcd.clear()

while True:
  lcd.move_to(0, 0)
  lcd.putstr("Select Angle:")
  lcd.move_to(0, 1)
  lcd.putstr(str(angle) + " Deg  ")
 
  if next_switch.value() == 0:
    angle += 45
    if angle > 180:
        angle = 0
    sleep(0.3)
    lcd.clear()
    lcd.putstr("Select Angle:")
    lcd.move_to(0, 1)
    lcd.putstr(str(angle) + " Deg  ")
  if select_switch.value() == 0:
    lcd.clear()
    lcd.putstr("Moving To:")
    lcd.move_to(0, 1)
    lcd.putstr(str(angle) + " Deg")
    my_servo.set_angle(angle)
    sleep(1.5)
    lcd.clear()
    lcd.putstr("Angle Set!")
    sleep(1)
    lcd.clear()