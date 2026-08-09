
# Import necessary modules and functions
from machine import Pin, PWM
from time import sleep

# Define Servo class
class Servo:

    # Define constants for the PWM signal
    PWM_FREQ = 50  # 50Hz for most standard servos

    # Define duty cycle values for 0 and 180 degrees
    MIN_DUTY = 2000
    MAX_DUTY = 8000

    # Define function to initialize servo
    def __init__(self, pin_num):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(self.PWM_FREQ)

    # Define function to set the servo angle
    def set_angle(self, angle):

        # Keep the angle within the valid range
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        # Convert the angle to a PWM duty cycle
        duty = int(
            self.MIN_DUTY +
            (angle / 180) *
            (self.MAX_DUTY - self.MIN_DUTY)
        )

        # Set the PWM duty cycle
        self.pwm.duty_u16(duty)

    # Define function to turn off servo PWM
    def deinit(self):
        self.pwm.deinit()
        
