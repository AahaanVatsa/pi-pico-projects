
# Import necessary modules and functions
from machine import Pin, I2C
from imu import MPU6050
from time import sleep, ticks_ms, ticks_diff
import motion

# Define MPU6050 variable
imu = None

gyro_bias = 0  # Starting rotational bias

# Define function to initialize and calibrate IMU
def init():
    global imu
    global gyro_bias

    # Initialize I2C connection with the MPU6050
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    imu = MPU6050(i2c, device_addr=0x68)

    # Allow time for the IMU to initialize
    sleep(2)

    # Calibrate gyroscope
    samples = 500
    gyro_bias = 0

    # Take multiple gyroscope readings while the robot is stationary
    for i in range(samples):
        gyro_bias += imu.gyro.z
        sleep(0.002)

    # Calculate the average gyroscope bias
    gyro_bias /= samples

    sleep(1)


# Define function to move the robot straight using P control
def move(duration, kp):
    base_speed = 35000

    current_angle = 0.0
    target_angle = 0.0

    last_time = ticks_ms()
    start_time = ticks_ms()

    # Continue moving until the requested duration has passed
    while ticks_diff(ticks_ms(), start_time) < duration * 1000:
        now = ticks_ms()
        dt_ms = ticks_diff(now, last_time)

        # Skip the loop if no time has passed
        if dt_ms <= 0:
            continue

        dt = dt_ms / 1000.0
        last_time = now

        # Calculate the current rotation rate
        gz = (imu.gyro.z - gyro_bias) * 57.2958

        # Ignore very small rotations
        if abs(gz) < 0.1:
            gz = 0

        # Calculate the current angle from the gyroscope
        current_angle += gz * dt

        # Calculate the error from the target angle
        error = target_angle - current_angle

        # Calculate the motor correction
        correction = kp * error

        # Adjust the left and right motor speeds
        left_speed = int(base_speed + correction)
        right_speed = int(base_speed - correction)

        # Keep left motor speed within the valid PWM range
        if left_speed < 0:
            left_speed = 0
        elif left_speed > 65535:
            left_speed = 65535

        # Keep right motor speed within the valid PWM range
        if right_speed < 0:
            right_speed = 0
        elif right_speed > 65535:
            right_speed = 65535

        # Enable both motors
        motion.M1.value(1)
        motion.M2.value(1)

        # Set the motor speeds
        motion.SM1.duty_u16(left_speed)
        motion.SM2.duty_u16(right_speed)

        sleep(0.01)

    # Stop the motors after the requested duration
    motion.stop()
    
