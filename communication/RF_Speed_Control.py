# Import necessary modules and functions
from machine import Pin
from time import sleep
import motion

# Initialize motors
motion.init()

# Define RF remote button pins
rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

# Define starting motor speed
speed = 32768

# Main loop
while True:
  # Read button states (HIGH/LOW)
  A = rf_A.value()
  B = rf_B.value()
  C = rf_C.value()
  D = rf_D.value()

  if A == 1: # Move forward
    motion.forward(speed)
  elif B == 1: # Move backward
    motion.backward(speed)
  elif C == 1: # Increase speed
    if speed < 65535:
      speed += 6500
  elif D == 1: # Decrease speed
    if speed > 32768:
      speed -= 6500
  else: # Stop robot
    motion.stop()
  sleep(0.5)
