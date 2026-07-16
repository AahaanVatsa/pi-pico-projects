#Import necessary modules
from machine import Pin, PWM, I2C
from time import sleep
from i2c_lcd import I2cLcd
import ultrasonic
import motion

#Initialize motors and ultrasonic sensor
motion.init()
ultrasonic.init()

#Initialize LCD
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

#Assign switch variables
select_switch = Pin(3, Pin.IN, Pin.PULL_UP)
next_switch = Pin(6, Pin.IN, Pin.PULL_UP)

#Assign IR Array variables
left_ir = Pin(18, Pin.IN)
center_ir = Pin(19, Pin.IN)
right_ir = Pin(20, Pin.IN)

#Assign buzzer variables
buzz = PWM(Pin(9), freq=1000)
buzz.duty_u16(0)

#Variables for classrom counting logic
classrooms = ['A', 'B', 'C']
classroom_count = 0
lines_detected_count = 0
total_stops = 4

#Variable for different states and selected class
state = "select"
selected_class = classrooms[classroom_count]

#Function for short buzzer beep
def beep_short():
    buzz.duty_u16(30000)
    sleep(0.1)
    buzz.duty_u16(0)

#Function for long buzzer beep
def beep_long():
    buzz.duty_u16(30000)
    sleep(0.3)
    buzz.duty_u16(0)

#Main loop
while True:
    distance = ultrasonic.get_distance() #Distance variable to detect obstacles

    #Check if switch is being pressed during select state
    if next_switch.value() == 0 and state == "select":

      #Loop back to first classroom in list after max index value is reached (3 items)
      if classroom_count == 2:
        classroom_count = 0
      else:
        classroom_count += 1

        selected_class = classrooms[classroom_count] #Assign selected class using index value of list

        #Print selected class
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Classroom")
        lcd.move_to(0, 1)
        lcd.putstr(selected_class)
        sleep(0.3)

    #Selects classroom and changes state to go
    if select_switch.value() == 0 and state == "select":
        state = "go"
        lines_detected_count = 0

        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Going to Class")
        sleep(0.5)

    #Code for 'go' state
    if state == "go":

        #Check for obstacles
        if distance <= 10:
            motion.stop()
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Obstacle Ahead")
            beep_short()
            continue

        #Classroom reached
        if center_ir.value() == 0 and left_ir.value() == 0 and right_ir.value() == 0:
            lines_detected_count += 1
            sleep(0.2)

        #Straight path
        elif center_ir.value() == 0:
            motion.forward()

        #Path turning left
        elif left_ir.value() == 0:
            motion.left()

        #Path turning right
        elif right_ir.value() == 0:
            motion.right()

        #No path
        else:
            motion.stop()

        #When lines detected is equal to classroom index value
        if lines_detected_count >= classroom_count + 1:
            motion.stop()
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Reached Classroom")
            lcd.move_to(0, 1)
            lcd.putstr(selected_class)
            beep_long()
            state = "return"
            lines_detected_count = 0
            sleep(0.5)

    #Code for 'reutrn' state
    elif state == "return":

        #Check for obstacles
        if distance <= 10:
            motion.stop()
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Obstacle")
            lcd.move_to(0, 1)
            lcd.putstr("Returning")
            beep_short()
            continue

        #Print status
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Returning...")

        #Classroom detected
        if center_ir.value() == 0 and left_ir.value() == 0 and right_ir.value() == 0:
            lines_detected_count += 1
            sleep(0.2)

        #Straight path
        elif center_ir.value() == 0:
            motion.forward()

        #Path turning left
        elif left_ir.value() == 0:
            motion.left()

        #Path turning right
        elif right_ir.value() == 0:
            motion.right()

        #No path
        else:
            motion.stop()

        #Check for gate reached
        if lines_detected_count >= (total_stops - classroom_count - 1):
            motion.stop()
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Reached Gate")
            beep_long()
            state = "select"
            lines_detected_count = 0
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Ready")
            sleep(0.5)


