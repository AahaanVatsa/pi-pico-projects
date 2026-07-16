from machine import Pin, time_pulse_us
from time import sleep_us

trig = None
echo = None

def init():
    global trig, echo
    trig = Pin(15, Pin.OUT)
    echo = Pin(14, Pin.IN)

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