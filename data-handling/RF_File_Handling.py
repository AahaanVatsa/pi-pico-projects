from machine import Pin
from time import sleep

rf_A = Pin(13, Pin.IN)
rf_B = Pin(20, Pin.IN)
rf_C = Pin(19, Pin.IN)
rf_D = Pin(18, Pin.IN)

log_file = '/rf_log.csv'

with open(log_file, 'a') as f:
  f.seek(0,0)
  if not f.read(1):
    f.write('SR NO., A, B, C, D\n')
sr_no = 1

while True:
  A = rf_A.value()
  B = rf_B.value()
  C = rf_C.value()
  D = rf_D.value()

  with open(log_file, 'a') as f:
    f.write(str(sr_no) + ',' + str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + '\n')

  print(str(sr_no) + ',' + str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + '\n')
  sleep(0.5)