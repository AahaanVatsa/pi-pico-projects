# Import necessary modules and functions
import bluetooth
import time
import motion
import straight_motion
from machine import Pin, ADC
import dht

# Initialize motors
motion.init()

# Define environmental sensor pins
dht_sensor = dht.DHT22(Pin(12))
mq135 = ADC(Pin(26))

# Define MQ135 constants
vcc = 3.3
rl = 20000
r0 = 30000

# Define safety limits for temperature, humidity, and air quality
temp_limit = 32
hum_limit = 80
air_limit = 1000

# Define BLE service and characteristic UUIDs
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    0x0010
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    0x0008
)

# Define Bluetooth and movement variables
connected = False
conn_handle = None
tx_handle = None
rx_handle = None
last_send_time = time.ticks_ms()
path = []
path_buffer = ""
manual_command = "S"
straight_kp = 170
path_step_time = 0.1
turn_time_90 = 0.4

# Define function to read MQ135 sensor
def read_mq135_ppm():
    adc_value = mq135.read_u16()
    voltage = (adc_value / 65535) * vcc

    if voltage <= 0:
        return 0

    rs = rl * ((vcc - voltage) / voltage)
    ratio = rs / r0

    if ratio <= 0:
        return 0

    ppm = 116.6020682 * (ratio ** -2.769034857)
    return round(ppm, 2)

# Define function to check environmental safety
def get_safety_status(temperature, humidity, air_ppm):
    if temperature > temp_limit:
        return 1, "DANGER: High Temp!"

    elif humidity > hum_limit:
        return 1, "DANGER: High Humidity!"

    elif air_ppm > air_limit:
        return 1, "DANGER: Smoke Detected!"

    else:
        return 0, "Status: Normal"

# Define function to execute one path command
def execute_path_command(action, value):
    motion.stop()
    time.sleep(0.2)

    if action == "A":
        duration = value * path_step_time
        straight_motion.move(duration, straight_kp)

    elif action == "T":
        angle = value

        # Calculate turn duration from the requested angle
        turn_time = abs(angle) / 90.0
        turn_time = turn_time * turn_time_90

        if angle > 0:
            motion.left()
        else:
            motion.right()

        time.sleep(turn_time)
        motion.stop()

# Define function to execute the stored path
def execute_path():
    for command in path:
        action = command[0]
        steps = command[1]

        execute_path_command(action, steps)

    motion.stop()

# Define function to convert path text into commands
def save_path_from_text(path_text):
    global path

    path = []

    # Remove the END marker from the path
    path_text = path_text.replace("END", "")

    commands = path_text.split(";")

    for command in commands:
        if command:
            direction_steps = command.split(",")

            if len(direction_steps) == 2:
                direction = direction_steps[0]
                steps = int(direction_steps[1])

                if direction == "A":
                    path.append(("A", steps))

                elif direction == "T":
                    path.append(("T", steps))

# Define function to advertise the Pico W over Bluetooth
def advertise():
    name = b"PicoW_Robot"

    # Create advertising data containing the robot name
    adv = b"\x02\x01\x06" + bytes((len(name) + 1, 0x09)) + name

    ble.gap_advertise(100000, adv_data=adv)

# Define function to handle Bluetooth events
def ble_irq(event, data):
    global connected, conn_handle, path_buffer, manual_command

    if event == 1:  # Connected
        conn_handle = data[0]
        connected = True
        path_buffer = ""
        manual_command = "S"

        print("Connected")

    elif event == 2:  # Disconnected
        connected = False
        conn_handle = None
        path_buffer = ""
        manual_command = "S"

        motion.stop()
        print("Disconnected")

        # Start advertising again after disconnecting
        advertise()

    elif event == 3:  # Data received
        incoming = ble.gatts_read(rx_handle).decode().strip()
        print("Received:", incoming)

        # Check for manual movement commands
        if incoming == "F":
            manual_command = "F"
            return

        elif incoming == "B":
            manual_command = "B"
            return

        elif incoming == "L":
            manual_command = "L"
            return

        elif incoming == "R":
            manual_command = "R"
            return

        elif incoming == "S":
            manual_command = "S"
            motion.stop()
            return

        elif incoming == "RUN":
            execute_path()
            return

        # Add received path data to the path buffer
        path_buffer = path_buffer + incoming

        # Save the path when END is received
        if "END" in path_buffer:
            save_path_from_text(path_buffer)
            path_buffer = ""

# Initialize Bluetooth
ble = bluetooth.BLE()
ble.active(True)
ble.irq(ble_irq)

# Register Bluetooth service and characteristics
((tx_handle, rx_handle),) = ble.gatts_register_services((
    (_UART_UUID, (_UART_TX, _UART_RX)),
))

# Start Bluetooth advertising
advertise()

# Initialize straight-line movement
print("Calibrating IMU...")
straight_motion.init()

print("Robot Ready")

# Main loop
while True:
    if connected:

        # Execute the current manual movement command
        if manual_command == "F":
            motion.forward()

        elif manual_command == "B":
            motion.backward()

        elif manual_command == "L":
            motion.left()

        elif manual_command == "R":
            motion.right()

        # Send environmental data every 2 seconds
        if time.ticks_diff(time.ticks_ms(), last_send_time) > 2000:
            dht_sensor.measure()

            temperature = round(dht_sensor.temperature(), 1)
            humidity = round(dht_sensor.humidity(), 1)
            air_ppm = read_mq135_ppm()

            # Check environmental safety
            safe_status, safety_message = get_safety_status(
                temperature,
                humidity,
                air_ppm
            )

            # Create message containing sensor data
            message = "T:{},H:{},A:{},SAFE:{},MSG:{}".format(
                temperature,
                humidity,
                air_ppm,
                safe_status,
                safety_message
            )

            # Send sensor data to the connected device
            ble.gatts_notify(conn_handle, tx_handle, message)

            print(message)

            last_send_time = time.ticks_ms()

    # Small delay between loop iterations
    time.sleep_ms(100)
