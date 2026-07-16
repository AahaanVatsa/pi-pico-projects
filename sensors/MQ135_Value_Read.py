from machine import ADC, Pin
from time import sleep

adc = ADC(Pin(26))
vcc = 3.3
rl = 20000
ro = 11077.47
reading = 100

def read_voltage():
  adc_voltage = adc.read_u16()
  voltage = (adc_voltage/65535)*vcc
  return voltage

def calculate_rs(voltage):
  if voltage == 0:
    return 0
  rs = rl *((vcc-voltage)/voltage)
  return rs

print("Calibrating...")
sleep(0.75)
print("Starting in 5 seconds...")
sleep(5)

rs_total = 0

for i in range(reading):
  voltage = read_voltage()
  rs = calculate_rs(voltage)
  rs_total += rs
  print(f"Reading {i+1}: RS = {round(rs, 2)}")
  sleep(0.5)

ro = rs_total/reading

print('\nCalibration Complete!')
print(f"RO = {round(ro, 2)}")

while True:
  value = sensor.read_u16()
  print(f'Sensor Reading: {value}')
  sleep(1)