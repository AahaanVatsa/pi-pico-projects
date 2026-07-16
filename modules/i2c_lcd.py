
# I2C LCD Library code
# i2c_lcd.py
# Merged library from LcdApi + I2C HAL (PCF8574)
# Works with Raspberry Pi Pico + I2C LCD (HD44780)

import utime
from machine import I2C

class LcdApi:
    """Generic API for HD44780 compatible character LCDs."""

    # Command set
    LCD_CLR             = 0x01
    LCD_HOME            = 0x02
    LCD_ENTRY_MODE      = 0x04
    LCD_ENTRY_INC       = 0x02
    LCD_ENTRY_SHIFT     = 0x01
    LCD_ON_CTRL         = 0x08
    LCD_ON_DISPLAY      = 0x04
    LCD_ON_CURSOR       = 0x02
    LCD_ON_BLINK        = 0x01
    LCD_MOVE            = 0x10
    LCD_MOVE_DISP       = 0x08
    LCD_MOVE_RIGHT      = 0x04
    LCD_FUNCTION        = 0x20
    LCD_FUNCTION_8BIT   = 0x10
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_10DOTS = 0x04
    LCD_FUNCTION_RESET  = 0x30
    LCD_CGRAM           = 0x40
    LCD_DDRAM           = 0x80

    LCD_RS_CMD          = 0
    LCD_RS_DATA         = 1
    LCD_RW_WRITE        = 0
    LCD_RW_READ         = 1

    def __init__(self, num_lines, num_columns):
        self.num_lines = min(num_lines, 4)
        self.num_columns = min(num_columns, 40)
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.hal_write_command(self.LCD_DDRAM | addr)

    def putchar(self, char):
        if char == '\n':
            if not self.implied_newline:
                self.cursor_x = self.num_columns
        else:
            self.hal_write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = (char != '\n')
        if self.cursor_y >= self.num_lines:
            self.cursor_y = 0
        self.move_to(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        for char in string:
            self.putchar(char)

    # HAL stubs (implemented by subclass)
    def hal_write_command(self, cmd): raise NotImplementedError
    def hal_write_data(self, data): raise NotImplementedError
    def hal_backlight_on(self): pass
    def hal_backlight_off(self): pass
    def hal_sleep_us(self, usecs): utime.sleep_us(usecs)


# ======================
# I2C HAL Implementation
# ======================

# PCF8574 pin mapping
MASK_RS = 0x01
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA      = 4

class I2cLcd(LcdApi):
    """I2C LCD driver using PCF8574 backpack."""

    E_PULSE_US = 1
    E_DELAY_US = 1
  
    # Function to create custom character at a specified location
    def create_custom_char(self, location, pattern):
        """Create a custom character in CGRAM (Character Generator RAM)."""
        self.hal_write_command(0x40 + (location << 3))  # Set CGRAM address
        for line in pattern:
            self.hal_write_data(line)

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = True

        # Wake up
        self._i2c_write_byte(0)
        utime.sleep_ms(20)

        # Initialization sequence
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION)  # set to 4-bit mode
        utime.sleep_ms(5)

        super().__init__(num_lines, num_columns)

        # Now send full function set (4-bit, 2 lines, 5x8 font)
        self.hal_write_command(self.LCD_FUNCTION |
                               self.LCD_FUNCTION_2LINES)

        # Display OFF, clear, entry mode, display ON
        self.hal_write_command(self.LCD_ON_CTRL)  # display off
        self.clear()
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)  # display ON

    def _i2c_write_byte(self, byte):
        self.i2c.writeto(self.i2c_addr, bytes([byte & 0xFF]))

    def _pulse(self, byte):
        self._i2c_write_byte(byte | MASK_E)
        utime.sleep_us(self.E_PULSE_US)
        self._i2c_write_byte(byte & ~MASK_E)
        utime.sleep_us(self.E_DELAY_US)

    def hal_write_init_nibble(self, nibble):
        byte = ((int(self.backlight) << SHIFT_BACKLIGHT) |
                (((nibble >> 4) & 0x0F) << SHIFT_DATA))
        self._pulse(byte)

    def hal_backlight_on(self):
        self.backlight = True
        self._i2c_write_byte(int(self.backlight) << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        self.backlight = False
        self._i2c_write_byte(0)

    def hal_write_command(self, cmd):
        self._write_byte(cmd, rs=0)

    def hal_write_data(self, data):
        self._write_byte(data, rs=MASK_RS)

    def _write_byte(self, value, rs=0):
        # high nibble
        byte = (rs |
                (int(self.backlight) << SHIFT_BACKLIGHT) |
                (((value >> 4) & 0x0F) << SHIFT_DATA))
        self._pulse(byte)

        # low nibble
        byte = (rs |
                (int(self.backlight) << SHIFT_BACKLIGHT) |
                ((value & 0x0F) << SHIFT_DATA))
        self._pulse(byte)

        if value <= 3:  # slow commands
            utime.sleep_ms(5)