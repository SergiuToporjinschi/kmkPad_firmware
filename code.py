import board 
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Press, Release, Tap
from kmk.modules.macros import Macros

from custom.module.desktop_connection import DesktopConnection
from custom.screen.sh1106_i2c import SH1106_I2C
from custom.module.joystick_key_press import JoystickHandler  
from custom.screen.screen import Screen

keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
keyboard.debug_enabled = True  

display = Screen(display=SH1106_I2C(board.GP20, board.GP21), 
    width=128, height=64, brightness=0.7, dim_time=1 * 60, dim_target=0.10, brightness_step=0.05, off_time=5 * 60,
    flip=False
)

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP17, board.GP16, board.GP18, False, 1),)

joystick = JoystickHandler()
joystick.pins = ((board.GP26, board.GP27, board.GP22, 270, 15),)
joystick.map = [(( KC.W, KC.S, KC.A, KC.D, KC.LSHIFT, KC.X),)]  # ⬆️⬇️⬅️➡️ 

keyboard.extensions = [display, MediaKeys()]
keyboard.modules = [joystick, encoder_handler, Macros(), Layers(), DesktopConnection()]

ctrl_Shift_F5 = KC.MACRO(Press(KC.LCTL), Press(KC.LSFT), Tap(KC.F5), Release(KC.LSFT), Release(KC.LCTL))
s = KC.MACRO("Wow, KMK is awesome!")

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,
        KC.FD(1), KC.N7, KC.DIS_BRI, KC.SK_INF1, KC.SK_INF2,
    ],
    [
        KC.F5, KC.N2, KC.N3, KC.N4, KC.N5,
        KC.FD(0), KC.A, KC.N8, KC.N9, KC.N0,
    ]
]

encoder_handler.map = [((KC.VOLU, KC.VOLD, KC.MUTE),)]

if __name__ == '__main__':
    keyboard.go()
