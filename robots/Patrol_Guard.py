#Imported necessary modules
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
from servo_lib import Servo
from i2c_lcd import I2cLcd
import motion
import ultrasonic

#Initializing components
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
ultrasonic.init()
my_servo = Servo(11)
buzz = PWM(Pin(9), freq = 1000)
buzz.duty_u16(0)
motion.init()

#Varibles for servo movement
scan_angle = 0 #Stores angle of servo motor
scan_direction = 1 #Keeps track of direction

#Function for servo scan
def scan_servo():
  global scan_angle, scan_direction
  my_servo.set_angle(scan_angle)
  scan_angle += scan_direction * 10 #Change the angle by 10 degrees
  if scan_angle <= 0:
    scan_angle = 0
    scan_direction = 1
  elif scan_angle >= 180:
    scan_angle = 180
    scan_direction = -1

  sleep(0.05)

#Main code
while True:
  motion.forward()
  for i in range(40):
    scan_servo()
    distance = ultrasonic.get_distance()
    lcd.move_to(4,0)
    lcd.putstr("Scanning")
    sleep(1)
    lcd.clear
    lcd.move_to(3,0)
    lcd.putstr("Angle: " + str(scan_angle))
    lcd.move_to(0,1)
    lcd.putstr("Distance: " + str(distance) + " cm")

    if 0 < distance <= 25:
      motion.stop()
      sleep(0.5)
      my_servo.set_angle(90)
      intruder_angle = scan_angle
      lcd.clear()
      lcd.move_to(1,0)
      lcd.putstr("INTRUDER ALERT")
      lcd.move_to(3,1)
      lcd.putstr("Angle: " + str(intruder_angle))
      if intruder_angle <= 90:
        turnTime = (90-intruder_angle) * (700/90)
        motion.right()
      else:
        turnTime = (intruder_angle-90) * (700/90)
        motion.left()
        
      lcd.clear()
      lcd.move_to(1,0)
      lcd.putstr("Chasing Target")
      
      sleep(turnTime/1000)
      motion.stop()
      sleep(0.5)
      motion.forward()
      sleep(0.6)
      motion.stop()
      while True:
        buzz.duty_u16(32768)
        sleep(0.5)
        buzz_u16(0)
        sleep(0.5)
  motion.stop()
  motion.left()
  sleep(1)
  motion.stop()
  sleep(0.5)
  