# Import necessary modules and functions
from machine import Pin, I2C
from imu import MPU6050
from time import sleep, ticks_ms, ticks_diff
import motion

# Initialize motors and MPU6050
motion.init()
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c, device_addr=0x68)

# Allow time for initialization
sleep(2)

# Define stabilization variables
samples = 500
gyro_bias = 0

# Take z-axis gyro readings for calibration
for i in range(samples):
gyro_bias += imu.gyro.z
sleep(0.002)

# Calculate the average gyro bias
gyro_bias /= samples
sleep(1)

# Define function to move the robot straight using proportional correction
def move_straight_pd(duration):
kp = 170  # Proportional gain used to calculate error correction
base_speed = 35000

current_angle = 0.0
target_angle = 0.0

last_time = ticks_ms()
start_time = ticks_ms()

# Continue moving until the specified duration has passed
while ticks_diff(ticks_ms(), start_time) < duration * 1000:
    now = ticks_ms()
    dt_ms = ticks_diff(now, last_time)
    dt = dt_ms / 1000
    last_time = now

    # Calculate the current rotation rate
    gz = (imu.gyro.z - gyro_bias) * 52.2958

    if abs(gz) < 0.1:
        gz = 0

    # Calculate the current angle from the gyro readings
    current_angle += gz * dt

    # Calculate the correction needed to maintain the target angle
    error = target_angle - current_angle
    correction = kp * error

    # Adjust motor speeds to correct the robot's direction
    left_speed = int(base_speed + correction)
    right_speed = int(base_speed - correction)

    # Keep motor speeds within the valid PWM range
    if left_speed < 0:
        left_speed = 0
    elif left_speed > 65535:
        left_speed = 65535

    if right_speed < 0:
        right_speed = 0
    elif right_speed > 65535:
        right_speed = 65535

    motion.M1.value(1)
    motion.M2.value(1)
    motion.SM1.duty_u16(right_speed)
    motion.SM2.duty_u16(left_speed)

    sleep(0.01)

motion.stop()

# Continuously run the straight-line movement
while True:
move_straight_pd(10)
sleep(2)
