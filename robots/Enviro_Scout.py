#Import necessary modules
from machine import Pin, ADC, PWM
from time import sleep
from i2c_lcd import I2cLcd, I2C
import network
import motion
from wifi_connection import RobotServer
import dht

#Initialize LCD 
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.clear()

#Declare WiFi Credentials
wifi_name = "WIFINAME"
wifi_password = "WIFIPWD"

#Initialize motors
motion.init()
motion.stop()

#Initialize environmental sensors
dht_sensor = dht.DHT22(Pin(12))
mq135 = ADC(Pin(26))

#Define LED pins
red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)

#Define buzzer pin and freq
buzzer = PWM(Pin(9))
buzzer.freq(1000)
buzzer.duty_u16(0)

#Constants for ppm conversion
vcc = 3.3
rl = 20000
r0 = 30000

#Thresholds for comparison and danger detection
temp_limit = 32
hum_limit = 80
air_limit = 1000

#Function for measuring ppm
def read_mq135_ppm():
    adc_value = mq135.read_u16() #Provides an analog value(0-65535)
    voltage = (adc_value / 65535) * vcc

    if voltage <= 0: #Avoids dividing by 0
        return 0

    rs = rl * ((vcc - voltage) / voltage) #Solves for sensor resistance
    ratio = rs / r0 #Calculate resistance ratio used to estimate PPM

    if ratio <= 0:
        return 0

    ppm = 116.6020682 * (ratio ** -2.769034857) #Estimate PPM using the MQ135 calibration equation
    return round(ppm, 2)

#Function for safety message and status
def get_safety_status(temperature, humidity, air_ppm):
  dangers = []
  
  if temperature > temp_limit:
    dangers.append("HIGH TEMP")
    
  if humidity > hum_limit:
    dangers.append("HIGH HUMIDITY")

  if air_ppm > air_limit:
    dangers.append("SMOKE")

  if len(dangers) > 0:
    return 1, "DANGER: " + ", ".join(dangers)

  return 0, "STATUS: NORMAL"

#Functions for buzzer states (ON and OFF)
def buzzer_on():
  buzzer.duty_u16(32768)

def buzzer_off():
  buzzer.duty_u16(0)

#Function for updating LED, buzzer, and LCD according to safety status
def update_alerts(temperature, humidity, air_ppm):
  dangers = []

  if temperature > temp_limit:
    dangers.append("TEMP")

  if humidity > hum_limit:
    dangers.append("HUM")

  if air_ppm > air_limit:
    dangers.append("SMOKE")

  #No dangers
  if len(dangers) == 0:
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("STATUS: NORMAL")
    
    green_led.value(1)
    red_led.value(0)
    buzzer_off()

  #One danger (Temp, Hum, Smoke)
  elif len(dangers) == 1:
    green_led.value(0)

    if "TEMP" in dangers:
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("HIGH TEMP")
      
      for i in range(3):
        red_led.value(1)
        buzzer_on()
        sleep(0.6)

        red_led.value(0)
        buzzer_off()
        sleep(0.6)


    elif "HUM" in dangers:
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("HIGH HUMIDITY")
      
      for i in range(5):
        red_led.value(1)
        buzzer_on()
        sleep(0.3)

        red_led.value(0)
        buzzer_off()
        sleep(0.3)


    elif "SMOKE" in dangers:
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("SMOKE ALERT")

      for i in range(10):
        red_led.value(1)
        buzzer_on()
        sleep(0.1)

        red_led.value(0)
        buzzer_off()
        sleep(0.1)



  #Multiple dangers
  else:
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("MULTIPLE")

    lcd.move_to(0,1)
    lcd.putstr("DANGERS")

    green_led.value(0)
    red_led.value(1)

    buzzer_on()

#Initialize and activate the Wi-Fi interface
wlan = network.WLAN(network.STA_IF) #STA_IF (Station Interface) allows the Pico W to connect to an existing Wi-Fi network
wlan.active(True)
wlan.connect(wifi_name, wifi_password)

print("Connecting...")

#Keeps trying until wlan.isconnected() is True
while not wlan.isconnected():
  sleep(0.5)

print("Robot IP:", wlan.ifconfig()[0])

#Create communication server for the webpage
robot = RobotServer()

#Turns on green LED to signal normal status
green_led.value(1)
red_led.value(0)

#Main loop
while True:
    command = robot.get_command() #Checks for user commands

    #Different commands to move robot
    if command == "F":
      motion.forward()

    elif command == "B":
      motion.backward()

    elif command == "L":
      motion.left()

    elif command == "R":
      motion.right()

    else:
      motion.stop()

    #Read temperature, humidity, and air quality
    dht_sensor.measure()

    temperature = round(dht_sensor.temperature(), 1)

    humidity = round(dht_sensor.humidity(), 1)

    air_ppm = read_mq135_ppm()

    #Determine safety status and message to send to the webpage
    safe_status, safety_message = get_safety_status(
        temperature,
        humidity,
        air_ppm
    )

    #Update buzzer, LED, and LCD accordingly
    update_alerts(
        temperature,
        humidity,
        air_ppm
    )

    #Send data to webpage
    robot.send_data(
        temperature,
        humidity,
        air_ppm,
        safe_status,
        safety_message
    )

