import board 

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from custom.module.layers import Layers

from custom.module.desktop_connection import DesktopConnection
from custom.desktop_app.config import ConfigHandler

keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.extensions = []
keyboard.modules = [Layers(), DesktopConnection()]


config = ConfigHandler(len(keyboard.col_pins) * len(keyboard.row_pins))
config.load_config()
keyboard.debug_enabled = config.debug_enabled

if config.media_keys_enabled:
    from kmk.extensions.media_keys import MediaKeys
    keyboard.extensions.append(MediaKeys())

if config.macro_keys_enabled:
    from kmk.modules.macros import Macros
    keyboard.modules.append(Macros())


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
    screen._config = config  # Ensure the screen has access to the configuration
    keyboard.extensions.append(screen)

encoder_handler = None
if config.encoder_enabled:
    from kmk.modules.encoder import EncoderHandler
    encoder_handler = EncoderHandler()
    encoder_handler.pins = ((board.GP3, board.GP4,  board.GP5, config.encoder_reversed, config.encoder_divisor),)
    keyboard.modules.append(encoder_handler)

joystickKey_handler = None
if config.joystick_enabled:
    from custom.module.joystick_key_press import JoystickKeyHandler  
    joystickKey_handler = JoystickKeyHandler()
    joystickKey_handler.pins = ((board.GP26, board.GP27, board.GP28, config.joystick_rotation, config.joystick_travel_segments),)
    keyboard.modules.append(joystickKey_handler)


keyMaps = config.layers_key_maps
keyboard.active_layers = list(range(len(keyMaps)))
keyboard.keymap = keyMaps

# encoder map 
if encoder_handler is not None:
    # encoder_handler.map = [[[KC.VOLD, KC.VOLU, KC.MUTE]], [[KC.TRNS, KC.TRNS, KC.TRNS]], [[KC.TRNS, KC.TRNS, KC.TRNS]], [[KC.TRNS, KC.TRNS, KC.TRNS]]]
    encoder_handler.map = config.layers_encoders_maps #⬅️➡️👇

# joystickKey map 
if joystickKey_handler is not None:
    joystickKey_handler.map = config.layers_joystick_keys_maps # ⬆️⬇️⬅️➡️🏃‍➡️👇


del config

if __name__ == '__main__': 
    keyboard.go()
