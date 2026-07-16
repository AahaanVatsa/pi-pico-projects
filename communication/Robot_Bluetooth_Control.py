from time import sleep_ms
import bluetooth
import motion

motion.init()

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), 0x0008)

connected = False
conn_handle = None
rx_handle = None

def advertise():
  name = b"PicoW Robot"
  adv = b"\x02\x01\x06" + bytes((len(name) + 1, 0x09))
  ble.gap_advertise(100,adv_data = adv)


def ble_irq(event,data):
  global connect,conn_handle
  if event == 1:
    conn_handle = data[0]
    connected = True
    print('Connected!')

  elif event == 2:
    connected = False
    conn_handle = None
    motion.stop()
    print('Disconnected!')
    advertise()

  elif event == 3:
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



ble = bluetooth.BLE()
ble.active(True)
ble.irq(ble_irq)

((rx_handle,),) = ble.gatts_register_services(((_UART_UUID, (_UART_RX,)),))
advertise()

while True:
  sleep_ms(100)

