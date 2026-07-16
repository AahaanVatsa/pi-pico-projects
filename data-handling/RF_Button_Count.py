from machine import Pin
from time import sleep

rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

count_A = 0
count_B = 0
count_C = 0
count_D = 0

while True:
  A = rf_A.value()
  B = rf_B.value()
  C = rf_C.value()
  D = rf_D.value()

  if A == 1:
    count_A += 1
  if B == 1:
    count_B += 1
  if C == 1:
    count_C += 1
  if D == 1:
    count_D += 1

  with open('/rf_count.csv', 'w') as f:
    f.write('Button, Count\n')
    f.write('A ,' + str(count_A) + '\n')
    f.write('B ,' + str(count_B) + '\n')
    f.write('C ,' + str(count_C) + '\n')
    f.write('D ,' + str(count_D) + '\n')

  print('Button Counts')
  print('A: ', count_A)
  print('B: ', count_B)
  print('C: ', count_C)
  print('D: ', count_D)
  print('--------------')

  sleep(0.2)