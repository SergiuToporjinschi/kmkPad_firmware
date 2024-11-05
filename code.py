import board 

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
# from kmk.modules.layers import Layers
from custom.module.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Press, Release, Tap
from kmk.modules.macros import Macros

from custom.module.desktop_connection import DesktopConnection
from custom.screen.sh1106_i2c import SH1106_I2C
from custom.module.joystick_key_press import JoystickHandler  
from custom.screen.screen import Screen
from custom.desktop_app.config import ConfigHandler



keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
keyboard.debug_enabled = True

config = ConfigHandler(len(keyboard.col_pins) * len(keyboard.row_pins))
config.load_config()

display = Screen(display=SH1106_I2C(board.GP20, board.GP21), 
    width=128, height=64, 
    brightness=config.screen_brightness, 
    dim_time=config.screen_dim_timeout, 
    dim_target=config.screen_dim_target, 
    brightness_step=config.screen_brightness_step, 
    off_time=config.screen_off_time,
    flip=config.screen_flip
)

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP3, board.GP4,  board.GP5, config.encoder_reversed, config.encoder_divisor),)

joystick = JoystickHandler()
joystick.pins = ((board.GP26, board.GP27, board.GP28, 270, 15),)
joystick.map = [(( KC.W, KC.S, KC.A, KC.D, KC.LSHIFT, KC.X),)]  # ⬆️⬇️⬅️➡️ 

keyboard.extensions = [display, MediaKeys()]
keyboard.modules = [joystick, encoder_handler, Macros(), Layers(), DesktopConnection()]

# ctrl_Shift_F5 = KC.MACRO(Press(KC.LCTL), Press(KC.LSFT), Tap(KC.F5), Release(KC.LSFT), Release(KC.LCTL))
# s = KC.MACRO("Wow, KMK is awesome!")

# keyMaps = [
keyMaps = [
    # [
    #     KC.TG(1), KC.N2, KC.N3, KC.N4, KC.N5,
    #     KC.F8, KC.F9, KC.LSHIFT(KC.F8), KC.F7, KC.F8,
    # ],
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

# print(f'{keyboard.active_layers}')

encoder_handler.map = config.layers_encoders_maps
# encoder_handler.map = [[[ KC.TGS('DOWN'), KC.TGS('UP'), KC.MUTE]],[[KC.TGS('DOWN'), KC.TGS('UP'), KC.TRNS]],[[KC.TGS('DOWN'), KC.TGS('UP'), KC.TRNS]]]


if __name__ == '__main__':
    keyboard.go()
