from time import sleep
import motion
import ultrasonic

motion.init()
ultrasonic.init()

speed_profile = 
{
  "STOP": 0,
  "LEVEL_1": 36000,
  "LEVEL_2": 46000,
  "LEVEL_3": 56000,
  "FULL": 65535
}

def get_speed(distance):
  if distance < 10:
    return speed_profile["STOP"]
  elif distance < 20:
    return speed_profile["LEVEL_1"]
  elif distance < 30:
    return speed_profile["LEVEL_2"]
  elif distance < 40:
    return speed_profile["LEVEL_3"]
  else:
    return speed_profile["FULL"]
    
while True:
  distance = ultrasonic.get_distance()
  speed = get_speed

  if speed == 0:
    motion.stop()
  else:
    motion.forward()

  sleep(0.2)