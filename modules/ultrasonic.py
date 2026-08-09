
# Import necessary modules and functions
from machine import Pin, time_pulse_us
from time import sleep_us

# Define ultrasonic variables
trig = None
echo = None

# Define function to initialize ultrasonic
def init(t, e):
    global trig, echo
    trig = Pin(t, Pin.OUT)
    echo = Pin(e, Pin.IN)

# Define function to read distance from ultrasonic
def get_distance():
    global trig, echo
    trig.low()
    sleep_us(2)
    trig.high()
    sleep_us(10)
    trig.low()
    duration = time_pulse_us(echo, 1)
    distance = duration * 0.0344 / 2
    return int(distance)
