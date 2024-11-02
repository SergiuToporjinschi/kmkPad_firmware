import busio

import adafruit_displayio_sh1106  # Display-specific library
import displayio

from kmk.extensions.display import DisplayBase

# Required to initialize this display
displayio.release_displays()


class SH1106_I2C(DisplayBase):
    def __init__(self, i2c=None, sda=None, sck=None, baudrate=1000000, device_address=0x3C):
        self.device_address = device_address
        self.baudrate = baudrate
        # i2c initialization
        self.i2c = i2c
        if self.i2c is None:
            self.i2c = busio.I2C(sck, sda)

    def during_bootup(self, width, height, rotation):
        self.display = adafruit_displayio_sh1106.SH1106(
            displayio.I2CDisplay(self.i2c, device_address=self.device_address),
            width=width,
            height=height,
            rotation=rotation,
        )

        return self.display

    def deinit(self):
        self.i2c.deinit()