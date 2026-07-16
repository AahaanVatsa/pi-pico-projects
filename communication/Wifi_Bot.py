from time import sleep
import network
import motion
from wifi_connection import RobotServer

WIFI_NAME = "Barsana_2"
WIFI_PASSWORD = "Co99ect2sa9"

motion.init()
motion.stop()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD)

print("Connecting...")
while not wlan.isconnected():
    sleep(0.5)

print("Robot IP:", wlan.ifconfig()[0])

robot = RobotServer()

while True:
    command = robot.get_command()

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