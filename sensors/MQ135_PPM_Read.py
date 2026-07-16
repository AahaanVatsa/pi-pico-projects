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

def calculate_ppm(rs):
  ratio = rs/ro
  ppm = 116.6020682*(ratio**-2.769034857)
  return ppm

while True:
  voltage = read_voltage()
  rs = calculate_rs(voltage)
  ppm = calculate_ppm(rs)

  print(f"Voltage: {round(voltage, 2)} ")
  print(f"RS: {round(rs, 2)} Ω")
  print(f"Estimated CO₂: {round(ppm, 2)} ppm")
  sleep(2)