#Import necessary modules
from machine import Pin, I2C, PWM
from time import sleep
from i2c_lcd import I2cLcd

#Initialize LCD
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

#Motor1 Connections
m1p = Pin(10,Pin.OUT)
m1n = Pin(9,Pin.OUT)
m1s = PWM(Pin(21),freq=1000)

#Motor2 Connections
m2p = Pin(8,Pin.OUT)
m2n = Pin(7,Pin.OUT)
m2s = PWM(Pin(22),freq=1000)

#IR Connections
ir_front = Pin(6, Pin.IN)
ir_left = Pin(3, Pin.IN)

#Variables
box_count = 0
box_detected = False
stock = 6
u_turn_done = False

#Fucntion to move robot forward
def forward():
  m1p.value(1)
  m1n.value(0)
  m2p.value(1)
  m2n.value(0)
  m1s.duty_u16(30000)
  m2s.duty_u16(32768)

#Function to stop robot
def stop_robot():
  m1s.duty_u16(0)
  m2s.duty_u16(0)

#Function to perform u-turn upon reaching first path end
def u_turn():
  m1p.value(1)
  m1n.value(0)
  m2p.value(0)
  m2n.value(1)
  m1s.duty_u16(30000)
  m2s.duty_u16(30000)
  sleep(1.5)
  stop_robot()
  sleep(0.5)

#Function to display count info on LCD Display
def show_count():
  lcd.clear()
  lcd.move_to(0,0)
  lcd.putstr("Total: ")
  lcd.putstr(str(stock))
  lcd.move_to(0,1)
  lcd.putstr("Current: ")
  lcd.putstr(str(box_count))

#Starting code
lcd.clear()
lcd.putstr("Inventory Start")
sleep(1)
lcd.clear()
show_count()
forward()

#Infinite loop
while True:
  
  #Checks if path end has been reached
  if ir_front.value() == 0:
    stop_robot()
    sleep(0.5)
    
    #Checks if u-turn has already been performed
    if not u_turn_done:
      u_turn()
      u_turn_done = True
      forward()
      sleep(0.1)
    else:
      stop_robot()
      lcd.clear()
      lcd.putstr("Inventory Over!")
      break
  else:
    forward()
    
  #Checks if box is detected
  if ir_left.value() == 0:
    if not box_detected:
      box_count += 1
      box_detected = True
      show_count()
  else:
    box_detected = False
    
  #Debounce delay
  sleep(0.1)
