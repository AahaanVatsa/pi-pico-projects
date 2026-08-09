# Import necessary modules and functions
from machine import Pin
from time import sleep
import ultrasonic
from servo_lib import Servo

# Define servo motor pin
servo_motor = Servo(11)

# Initialize ultrasonic sensor
ultrasonic.init(15, 14)

# Define RF remote button pins
rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)

# Define motor speed
speed = 32768

# Define starting angle
angle = 90

servo_motor.set_angle(angle)

sleep(0.75) # Small delay to complete initialization

# Main loop
while True:
  # Read button states (HIGH/LOW)
  A = rf_A.value()
  B = rf_B.value()
  distance = ultrasonic.get_distance() # Measure distance
  servo_motor.set_angle(angle) # Set servo to current angle value
  print("Distance: ", distance, " cm", " | Servo Angle: ", angle)
  if A == 1: # Turn towards 0 degrees
    if angle > 0:
      angle -= 10
  if B == 1: # Turn towards 180 degress
    if angle < 180:
      angle += 10
  sleep(0.5)
