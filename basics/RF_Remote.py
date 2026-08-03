# Import necessary modules and functions
from machine import Pin
from time import sleep

# Initialize RF remote buttons
rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

# Continuously check and display button values
while True:
A = rf_A.value()
B = rf_B.value()
C = rf_C.value()
D = rf_D.value()

print("A: ", A, " B: ", B, " C: ", C, " D: ", D)
sleep(0.5)
