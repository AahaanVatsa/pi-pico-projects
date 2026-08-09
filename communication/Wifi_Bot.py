# Import necessary modules and functions
from time import sleep
import network
import motion
from wifi_connection import RobotServer

# Define WiFi credentials
WIFI_NAME = "URWIFINAME"
WIFI_PASSWORD = "URWIFIPWD"

# Intialize and stop motors
motion.init()
motion.stop()

# Initialize and connect to WiFi
wlan = network.WLAN(network.STA_IF) # Create station interface(WiFi client)
wlan.active(True)
wlan.connect(WIFI_NAME, WIFI_PASSWORD)

# Keep trying until connected
print("Connecting...")
while not wlan.isconnected():
    sleep(0.5)

print("Robot IP:", wlan.ifconfig()[0]) # Print robot IP address

robot = RobotServer() # Create an object 'robot' of class RobotServer

# Main loop
while True:
    command = robot.get_command() # Receive command from web dashboard

    if command == "F": # Move forward
        motion.forward()
    elif command == "B": # Move backward
        motion.backward()
    elif command == "L": # Move left
        motion.left()
    elif command == "R": # Move right
        motion.right()
    else: # Stop robot
        motion.stop()
