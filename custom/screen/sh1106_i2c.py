import busio
import board  # Add this import
from .drv_sh1106 import SH1106
import displayio
from kmk.utils import Debug
from kmk.extensions.display import DisplayBase

# Required to initialize this display
displayio.release_displays()

debug = Debug(__name__)

class SH1106_I2C(DisplayBase):
    def __init__(self, sda=None, sck=None, i2c=None, device_address=0x3C):
        self.device_address = device_address
        # i2c initialization
        self.i2c = i2c
        if self.i2c is None:
            self.i2c = busio.I2C(sck or board.SCL, sda or board.SDA)  # Use board pins if not provided
        self.display = None  # Initialize display attribute

    def during_bootup(self, width: int, height: int, rotation: int):
        self.display = SH1106(
            displayio.I2CDisplay(self.i2c, device_address=self.device_address),
            width=width,
            height=height,
            rotation=rotation,
        )
        return self.display

    def deinit(self):
        self.i2c.deinit()
