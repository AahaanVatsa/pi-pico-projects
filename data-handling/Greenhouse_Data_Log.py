from machine import Pin, ADC
from time import sleep, ticks_ms
import dht

#Sensors
dht_sensor = dht.DHT22(Pin(12))
adc = ADC(Pin(26))

#Constants
vcc = 3.3
rl = 20000
ro = 30000

log_file = 'data.csv'

#Time Setup
print('Set Current Time')
start_hr = int(input('Enter Hour (0-23): '))
start_min = int(input('Enter Minutes (0-59): '))
start_sec = int(input('Enter Seconds (0-59): '))

start_time_seconds = start_hr * 3600 + start_min * 60 + start_sec
start_ticks = ticks_ms()

def get_time():
    elapsed_seconds = (ticks_ms() - start_ticks) // 1000
    total = (start_time_seconds + elapsed_seconds) % 86400

    hrs = total // 3600
    mins = (total % 3600) // 60
    secs = total % 60

    return "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)

#Sensor Functions
def read_voltage():
    return (adc.read_u16() / 65535) * vcc

def calculate_rs(voltage):
    if voltage == 0:
        return rl * 10
    return rl * (vcc - voltage) / voltage

def calculate_ppm(rs):
    ratio = rs / ro
    return 116.6020682 * (ratio ** -2.769034857)

#CSV Setup
try:
    with open(log_file, "r") as f:
        pass
except:
    with open(log_file, "w") as f:
        f.write("SrNo,Time,Temperature,Humidity,PPM\n")

#Main loop
sr_no = 1

while True:
    #DHT Safe Read
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except:
        temp = -1
        humidity = -1

    #MQ135 Sensor
    voltage = read_voltage()
    rs = calculate_rs(voltage)
    ppm = calculate_ppm(rs)

    #Time
    time_now = get_time()

    #Log
    with open(log_file, 'a') as f:
        f.write("{},{},{},{},{}\n".format(sr_no, time_now, temp, humidity, int(ppm)))

    print('Saved:', sr_no, time_now, temp, humidity, int(ppm))

    sr_no += 1
    sleep(2)