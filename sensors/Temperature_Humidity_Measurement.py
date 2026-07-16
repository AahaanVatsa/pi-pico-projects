from machine import Pin, I2C
from i2c_lcd import I2cLcd
from time import sleep
import dht

dht_sensor = dht.DHT22(Pin(12))

i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

while True:
  dht_sensor.measure()
  temp = round(dht_sensor.temperature(), 1)
  humidity = round(dht_sensor.humidity(), 1)

  lcd.clear()
  lcd.move_to(0,0)
  lcd.putstr(f"Temp: {temp} C")
  lcd.move_to(0,1)
  lcd.putstr(f"Humidity: {humidity} %")
  sleep(1)
