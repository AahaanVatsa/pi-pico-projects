
from machine import Pin, I2C
from imu import MPU6050
from time import sleep, ticks_ms, ticks_diff
import motion

imu = None
gyro_bias = 0

# Initialize Sensor + Calibration
def init():
  global imu
  global gyro_bias

  i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
  imu = MPU6050(i2c, device_addr=0x68)

  sleep(2)

  # ---- GYRO CALIBRATION ----
  samples = 500
  gyro_bias = 0

  for i in range(samples):
    gyro_bias += imu.gyro.z
    sleep(0.002)

  gyro_bias /= samples

  sleep(1)

# Move Straight using P Control
def move(duration, kp):
  base_speed = 35000

  current_angle = 0.0
  target_angle = 0.0

  last_time = ticks_ms()
  start_time = ticks_ms()

  while ticks_diff(ticks_ms(), start_time) < duration * 1000:
    now = ticks_ms()
    dt_ms = ticks_diff(now, last_time)

    if dt_ms <= 0:
      continue

    dt = dt_ms / 1000.0
    last_time = now

    gz = (imu.gyro.z - gyro_bias) * 57.2958

    if abs(gz) < 0.1:
      gz = 0

    current_angle += gz * dt

    error = target_angle - current_angle
    correction = kp * error

    left_speed = int(base_speed + correction)
    right_speed = int(base_speed - correction)

    # ----- SPEED LIMITING USING IF-ELSE -----
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

    motion.SM1.duty_u16(left_speed)
    motion.SM2.duty_u16(right_speed)

    sleep(0.01)

  motion.stop()
    

    