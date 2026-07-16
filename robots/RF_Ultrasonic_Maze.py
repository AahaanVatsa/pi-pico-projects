from machine import Pin
from time import sleep
import ultrasonic
import motion

motion.init()
ultrasonic.init()

rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

with open('/rf_ultrasonic_maze.csv', 'a') as f:
    f.seek(0,0)
    if not f.read(1):
      f.write('Serial No, Distance, A, B, C, D\n')
    sr_no = 1
  
while True:
  A = rf_A.value()
  B = rf_B.value()
  C = rf_C.value()
  D = rf_D.value()
  distance = ultrasonic.get_distance()

  if A == 1:
    motion.forward()
  elif B == 1:
    motion.right()
  elif C == 1:
    motion.left()
  elif D == 1:
    motion.backward()
  else:
    motion.stop()
  
  with open('/rf_ultrasonic_maze.csv', 'a') as f:
    f.write(str(sr_no) + ',' str(distance) + ',' + str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + '\n')

  print('Serial No, Distance, A, B, C, D')
  print(str(sr_no) + ',' str(distance) + ',' + str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + '\n')
  sr_no += 1

  sleep(0.5)
