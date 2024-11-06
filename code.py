import board 

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from custom.module.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Macros

from custom.module.desktop_connection import DesktopConnection
from custom.desktop_app.config import ConfigHandler

keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.extensions = [MediaKeys()]
keyboard.modules = [Macros(), Layers(), DesktopConnection()]

config = ConfigHandler(len(keyboard.col_pins) * len(keyboard.row_pins))
config.load_config()
keyboard.debug_enabled = config.debug_enabled

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

# Key map
keyMaps = [
    [
        KC.TG(1), KC.N2, KC.N3, KC.N4, KC.N5,
        KC.F8, KC.F9, KC.LSHIFT(KC.F8), KC.F7, KC.F8,
    ],
    [
        KC.TGS('UP'), KC.N2, KC.N3, KC.N4, KC.N5,
        KC.A, KC.B, KC.LSHIFT(KC.F8), KC.F7, KC.N0,
    ],
    [
        KC.TGS('UP'), KC.N2, KC.N3, KC.N4, KC.TRNS,
        KC.F, KC.A, KC.N8, KC.N9, KC.N1,
    ],
    [
        KC.TGS('UP'), KC.N2, KC.N3, KC.N4, KC.TRNS,
        KC.D, KC.A, KC.N8, KC.N9, KC.N2,
    ]
] + config.layers_key_maps

keyboard.active_layers = list(range(len(keyMaps)))
keyboard.keymap = keyMaps

# encoder map 
if encoder_handler is not None:
    encoder_handler.map = config.layers_encoders_maps

# joystickKey map 
if joystickKey_handler is not None:
    joystickKey_handler.map = [(( KC.W, KC.S, KC.A, KC.D, KC.LSHIFT, KC.X),)]  # ⬆️⬇️⬅️➡️ 

del config

if __name__ == '__main__':
    keyboard.go()
