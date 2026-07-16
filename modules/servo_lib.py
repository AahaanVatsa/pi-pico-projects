
from machine import Pin, PWM
from time import sleep

class Servo:  
    # Constants for the PWM signal
    PWM_FREQ = 50  # 50Hz for most standard servos
    
    # Duty cycle values for 0 and 180 degrees
    MIN_DUTY = 2000
    MAX_DUTY = 8000

    def __init__(self, pin_num):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(self.PWM_FREQ)

    def set_angle(self, angle):
        # Clamp the angle to the valid range
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
            
        # Map the angle to the duty cycle range
        duty = int(self.MIN_DUTY + (angle / 180) * (self.MAX_DUTY - self.MIN_DUTY))
        
        # Set the PWM duty cycle
        self.pwm.duty_u16(duty)

    def deinit(self):
        self.pwm.deinit()