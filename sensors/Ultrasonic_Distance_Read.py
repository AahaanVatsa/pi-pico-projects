from time import sleep
import ultrasonic

ultrasonic.init()

while True:
  distance = ultrasonic.get_distance()
  print(distance)
  sleep(0.75)