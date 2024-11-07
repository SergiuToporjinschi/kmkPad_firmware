import board 

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from custom.module.layers import Layers

from custom.module.desktop_connection import DesktopConnection
from custom.desktop_app.config import ConfigHandler

config = ConfigHandler()


keyboard = KMKKeyboard()
keyboard.col_pins = config.keyboard_GPIO_pin_cols
keyboard.row_pins = config.keyboard_GPIO_pin_rows
keyboard.diode_orientation = config.keyboard_diode_orientation

keyboard.extensions = []
keyboard.modules = [Layers(), DesktopConnection()]
keyboard.debug_enabled = config.debug_enabled

if config.media_keys_enabled:
    from kmk.extensions.media_keys import MediaKeys
    keyboard.extensions.append(MediaKeys())

if config.macro_keys_enabled:
    from kmk.modules.macros import Macros
    keyboard.modules.append(Macros())

# ----------------------------------------------------screen
if config.screen_enabled:
    from custom.screen.screen import Screen
    from custom.screen.sh1106_i2c import SH1106_I2C
    screen = Screen(display=SH1106_I2C(board.GP20, board.GP21), 
        width=config.screen_width, height=config.screen_height, 
        brightness=config.screen_brightness, 
        dim_time=config.screen_dim_timeout, 
        dim_target=config.screen_dim_target, 
        brightness_step=config.screen_brightness_step, 
        off_time=config.screen_off_time,
        flip=config.screen_flip
    )
    screen.config = config  # Ensure the screen has access to the configuration
    keyboard.extensions.append(screen)

# ----------------------------------------------------encoder
encoder_handler = None
if config.encoder_enabled:
    from kmk.modules.encoder import EncoderHandler
    encoder_handler = EncoderHandler()
    enc_config = config.encoder_GPIO_pins
    enc_config += (config.encoder_reversed, config.encoder_divisor)
    encoder_handler.pins = (enc_config,)
    keyboard.modules.append(encoder_handler)

# ----------------------------------------------------joystickKey
joystickKey_handler = None
if config.joystickKey_enabled:
    from custom.module.joystick_key_press import JoystickKeyHandler  
    joystickKey_handler = JoystickKeyHandler()
    joy_config = config.joystickKey_GPIO_pins
    joy_config += (config.joystickKey_rotation, config.joystickKey_travel_segments)
    joystickKey_handler.pins = (joy_config,)
    keyboard.modules.append(joystickKey_handler)

# ----------------------------------------------------layers
keyMaps = config.layers_key_maps
keyboard.active_layers = list(range(len(keyMaps)))
keyboard.keymap = keyMaps

# encoder map 
if encoder_handler is not None:
    encoder_handler.map = config.layers_encoders_maps #⬅️➡️👇

# joystickKey map 
if joystickKey_handler is not None:
    joystickKey_handler.map = config.layers_joystickKeys_maps # ⬆️⬇️⬅️➡️🏃‍➡️👇


del config

if __name__ == '__main__': 
    keyboard.go()
