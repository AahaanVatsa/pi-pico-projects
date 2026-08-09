# Import necessary modules and functions
from time import sleep_ms
import bluetooth
import motion

# Initialize motors
motion.init()

# Define BLE service and characteristic UUIDs
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), 0x0008)

# Define Bluetooth variables
connected = False
conn_handle = None
rx_handle = None

# Define function to advertise the Pico W over Bluetooth
def advertise():
  name = b"PicoW Robot"
  adv = b"\x02\x01\x06" + bytes((len(name) + 1, 0x09))
  ble.gap_advertise(100,adv_data = adv)

# Define function to handle Bluetooth events
def ble_irq(event,data):
  global connect,conn_handle
  
  if event == 1: # Connected
    conn_handle = data[0]
    connected = True
    print('Connected!')

  elif event == 2: # Disconnected
    connected = False
    conn_handle = None
    motion.stop()
    print('Disconnected!')
    advertise()

  elif event == 3: # Data received
    incoming = ble.gatts_read(rx_handle).decode().strip()
    print('Received: ', incoming)
    if incoming == 'F':
      motion.forward()
    elif incoming == 'B':
      motion.backward()
    elif incoming == 'L':
      motion.left()
    elif incoming == 'R':
      motion.right()
    elif incoming == 'S':
      motion.stop()


# Initialize Bluetooth
ble = bluetooth.BLE()
ble.active(True)
ble.irq(ble_irq)

# Register RX (receive data/command) and advertise
((rx_handle,),) = ble.gatts_register_services(((_UART_UUID, (_UART_RX,)),))
advertise()

# Main loop (add delay between commands and advertisement)
while True:
  sleep_ms(100)
