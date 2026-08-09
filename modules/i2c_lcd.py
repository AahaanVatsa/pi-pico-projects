
# Import necessary modules and functions
import utime
from machine import I2C

# Define LCD API class
class LcdApi:
    """Generic API for HD44780 compatible character LCDs."""

    # Define LCD command constants
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

    # Define LCD register and read/write constants
    LCD_RS_CMD          = 0
    LCD_RS_DATA         = 1
    LCD_RW_WRITE        = 0
    LCD_RW_READ         = 1

    # Define function to initialize LCD
    def __init__(self, num_lines, num_columns):
        self.num_lines = min(num_lines, 4)
        self.num_columns = min(num_columns, 40)
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True

    # Define function to clear LCD
    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    # Define function to move cursor to specific location
    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y

        addr = cursor_x & 0x3F

        if cursor_y & 1:
            addr += 0x40

        if cursor_y & 2:
            addr += self.num_columns

        self.hal_write_command(self.LCD_DDRAM | addr)

    # Define function to display a single char on LCD
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

    # Define function to display string on LCD
    def putstr(self, string):
        for char in string:
            self.putchar(char)

    # Define functions for communication with LCD
    def hal_write_command(self, cmd):
        raise NotImplementedError

    def hal_write_data(self, data):
        raise NotImplementedError

    def hal_backlight_on(self):
        pass

    def hal_backlight_off(self):
        pass

    # Pause for a specified amount of time
    def hal_sleep_us(self, usecs):
        utime.sleep_us(usecs)


# Define I2C pin mapping for the PCF8574
MASK_RS = 0x01
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


# Define I2C LCD class
class I2cLcd(LcdApi):
    """I2C LCD driver using PCF8574 backpack."""

    E_PULSE_US = 1
    E_DELAY_US = 1

    # Define function to create a custom character
    def create_custom_char(self, location, pattern):
        """Create custom character in CGRAM."""

        self.hal_write_command(0x40 + (location << 3))

        for line in pattern:
            self.hal_write_data(line)

    # Define function to initialize I2C LCD
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = True

        # Wake up LCD
        self._i2c_write_byte(0)
        utime.sleep_ms(20)

        # Initialize the LCD
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(5)

        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)

        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)

        # Set the LCD to 4-bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        utime.sleep_ms(5)

        super().__init__(num_lines, num_columns)

        # Configure the LCD for 4-bit, 2-line, 5x8 font mode
        self.hal_write_command(
            self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES
        )

        # Turn the display off and clear the LCD
        self.hal_write_command(self.LCD_ON_CTRL)
        self.clear()

        # Set entry mode and turn the display on
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY
        )

    # Send one byte of data through I2C
    def _i2c_write_byte(self, byte):
        self.i2c.writeto(
            self.i2c_addr,
            bytes([byte & 0xFF])
        )

    # Send an enable pulse to the LCD
    def _pulse(self, byte):
        self._i2c_write_byte(byte | MASK_E)
        utime.sleep_us(self.E_PULSE_US)

        self._i2c_write_byte(byte & ~MASK_E)
        utime.sleep_us(self.E_DELAY_US)

    # Send the initial LCD setup command
    def hal_write_init_nibble(self, nibble):
        byte = (
            (int(self.backlight) << SHIFT_BACKLIGHT) |
            (((nibble >> 4) & 0x0F) << SHIFT_DATA)
        )

        self._pulse(byte)

    # Turn the LCD backlight on
    def hal_backlight_on(self):
        self.backlight = True
        self._i2c_write_byte(
            int(self.backlight) << SHIFT_BACKLIGHT
        )

    # Turn the LCD backlight off
    def hal_backlight_off(self):
        self.backlight = False
        self._i2c_write_byte(0)

    # Send a command to the LCD
    def hal_write_command(self, cmd):
        self._write_byte(cmd, rs=0)

    # Send character data to the LCD
    def hal_write_data(self, data):
        self._write_byte(data, rs=MASK_RS)

    # Send a byte of data to the LCD
    def _write_byte(self, value, rs=0):

        # Send the high 4 bits
        byte = (
            rs |
            (int(self.backlight) << SHIFT_BACKLIGHT) |
            (((value >> 4) & 0x0F) << SHIFT_DATA)
        )

        self._pulse(byte)

        # Send the low 4 bits
        byte = (
            rs |
            (int(self.backlight) << SHIFT_BACKLIGHT) |
            ((value & 0x0F) << SHIFT_DATA)
        )

        self._pulse(byte)

        # Wait longer for slow LCD commands
        if value <= 3:
            utime.sleep_ms(5)
