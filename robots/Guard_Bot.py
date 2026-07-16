#Imported necessary modules
from machine import Pin, PWM, I2C
from time import sleep
from servo_lib import Servo
from i2c_lcd import I2cLcd
from imu import MPU6050
import motion
import ultrasonic

#IR Sensor
ir1 = Pin(6, Pin.IN)
ir2 = Pin(3, Pin.IN)

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

lcd = I2cLcd(i2c, 0x27, 2, 16)

#Car Motor, Ultrasonic
ultrasonic.init()
motion.init()

#Servo Motor
my_servo = Servo(11)

#Buzzer
buzz = PWM(Pin(9), freq=1000)
buzz.duty_u16(0)

#Tilt Sensor
imu = MPU6050(i2c, device_addr = 0x68)
tilt_threshold = 1.5

#Servo variables to scan
scan_angle = 0
scan_direction = 1

#Variables for main logic
state = "PATROL"
rounds_completed = 0
max_rounds = 5

#Function to check if robot is tilted
def robot_tilted():
    gx = round(imu.gyro.x, 2)
    gy = round(imu.gyro.y, 2)
    if gx > tilt_threshold or gx < -tilt_threshold:
        return True
    if gy > tilt_threshold or gy < -tilt_threshold:
        return True
    return False

#Function for buzzer alert
def alert_buzz():
    for i in range(5):
        buzz.duty_u16(32768)
        sleep(0.2)
        buzz.duty_u16(0)
        sleep(0.2)

#Function for tamper alert
def tamper_buzz():
    for i in range(10):
        buzz.duty_u16(45000)
        sleep(0.1)
        buzz.duty_u16(0)
        sleep(0.1)

#Function for LCD output
def show_status(line1, line2=""):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(line1)
    lcd.move_to(0,1)
    lcd.putstr(line2)

#Function for servo scan
def scan_servo():
  global scan_angle, scan_direction
  my_servo.set_angle(scan_angle)
  scan_angle += scan_direction * 10
  if scan_angle <= 0:
    scan_angle = 0
    scan_direction = 1
  elif scan_angle >= 180:
    scan_angle = 180
    scan_direction = -1

#Patrol mode
def patrol():
    global rounds_completed, state
    show_status("Patrolling", "Round: " + str(rounds_completed))
    motion.uturn()
    motion.forward()
    for i in range(30):
        if robot_tilted():
            state = "TAMPER"
            return state
        scan_servo()
        distance = ultrasonic.get_distance()
        lcd.move_to(0,0)
        lcd.putstr("Scanning       ")
        lcd.move_to(0,1)
        lcd.putstr("Distance: " + str(distance) + " cm   ")
        if 0 < distance <= 25:
            state = "CHASE"
            return state
        sleep(0.1)
    rounds_completed += 1
    motion.uturn()
    if rounds_completed >= max_rounds:
        state = "RETURN"

#Chase mode
def chase():
    global state
    show_status("INTRUDER!", "Chasing")
    alert_buzz()
    my_servo.set_angle(90)
    
    chase_counter = 0
    max_chase_steps = 50
    
    while chase_counter < max_chase_steps:
        if robot_tilted():
            state = "TAMPER"
            return state
        left = ir1.value()
        right = ir2.value()
        dist = ultrasonic.get_distance()
        
        show_status("Chasing", "Dist: " + str(dist) + " cm")
        
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
            break
        chase_counter += 1
        sleep(0.1)
    
    state = "PATROL"

#Fucntion to return to charger
def return_to_charge():
    show_status("Returning", "To Charger")
    if rounds_completed % 2 != 0:
      motion.uturn()
    motion.forward()
    sleep(3)
    motion.stop()
    global state
    state = "CHARGING"

#Fucntion to enable charging mode
def charging():
    global state
    show_status("Charging Mode", "Please Wait")
    for i in range(10):
        if robot_tilted():
            state = "TAMPER"
            return state
        buzz.duty_u16(20000)
        sleep(0.3)
        buzz.duty_u16(0)
        sleep(0.7)
    global rounds_completed
    rounds_completed = 0
    state = "PATROL"

#Tamper mode
def tamper():
    motion.stop()
    show_status("TAMPER ALERT!", "Robot Moved!")
    tamper_buzz()
    while robot_tilted():
        sleep(0.2)
    global state
    state = "PATROL"

#Main loop
while True:
    if state == "PATROL":
        patrol()
    elif state == "CHASE":
        chase()
    elif state == "RETURN":
        return_to_charge()
    elif state == "CHARGING":
        charging()
    elif state == "TAMPER":
        tamper()
    sleep(0.1)
