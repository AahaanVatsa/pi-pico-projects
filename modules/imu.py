
import time

class Vector3:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.z = 0

class MPU6050:
  def __init__(self, i2c, device_addr=0x68):
    self.i2c = i2c
    self.addr = device_addr

    self._accel = Vector3()
    self._gyro = Vector3()

    # Wake up MPU6050
    self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
    time.sleep(0.1)

  def _read_word(self, reg):
    data = self.i2c.readfrom_mem(self.addr, reg, 2)
    value = (data[0] << 8) | data[1]
    if value > 32767:
      value -= 65536
    return value

  def _update_accel(self):
    ax = self._read_word(0x3B)
    ay = self._read_word(0x3D)
    az = self._read_word(0x3F)

    self._accel.x = (ax / 16384) * 9.81
    self._accel.y = (ay / 16384) * 9.81
    self._accel.z = (az / 16384) * 9.81

  def _update_gyro(self):
    gx = self._read_word(0x43)
    gy = self._read_word(0x45)
    gz = self._read_word(0x47)

    self._gyro.x = gx / 131
    self._gyro.y = gy / 131
    self._gyro.z = gz / 131

  @property
  def accel(self):
    self._update_accel()
    return self._accel

  @property
  def gyro(self):
    self._update_gyro()
    return self._gyro