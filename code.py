import board 
import displayio
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, Key, KeyAttrDict, ConsumerKey, MouseKey, ModifierKey, KeyboardKey, ModifiedKey
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers, LayerKey
from kmk.extensions.display import Display
from kmk.extensions.display import TextEntry
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Press, Release, Tap
from kmk.modules.macros import Macros
from kmk.modules.holdtap import HoldTap

from custom.module.desktop_connection import DesktopConnection
from custom.display.sh1106_i2c import SH1106_I2C
from custom.module.joystick_key_press import JoystickHandler  
from custom.display.screen import Screen

keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
keyboard.debug_enabled = True  

ssd1306Inst = SH1106_I2C(busio.I2C(board.GP21, board.GP20))
display = Display(
    display=ssd1306Inst, width=128, height=64, entries=[], brightness=0.5,
    dim_time=2, dim_target=0.1, brightness_step=0.01, off_time=20,
    flip=False, powersave_dim_time=2, powersave_dim_target=0.01, powersave_off_time=20
)

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP17, board.GP16, board.GP18, False, 1),)

joystick = JoystickHandler()
joystick.pins = ((board.GP27, board.GP26, board.GP22, 90),)
joystick.map = [((KC.W, KC.S, KC.A, KC.D, KC.X),)]  # ⬆️⬇️⬅️➡️ 

keyboard.extensions = [display, MediaKeys(), Screen()]
keyboard.modules = [joystick, encoder_handler, Macros(), Layers(), DesktopConnection(), HoldTap()]

ctrl_Shift_F5 = KC.MACRO(Press(KC.LCTL), Press(KC.LSFT), Tap(KC.F5), Release(KC.LSFT), Release(KC.LCTL))
s = KC.MACRO("Wow, KMK is awesome!")

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,
        KC.N6, KC.N7, KC.N8, KC.N9, KC.N9,
    ],
    [
        KC.get('F5'), KC.N2, KC.N3, KC.N4, KC.N5,
        KC.LCTRL(KC.LSFT(KC.F5)), KC.N7, KC.N8, KC.N9, KC.N0,
    ]
]

encoder_handler.map = [((KC.VOLU, KC.VOLD, KC.MUTE),)]

display.entries = [
    TextEntry(text="Basic", x=0, y=0, layer=0),
    TextEntry(text="Row: 1", x=0, y=12),
]

if __name__ == '__main__':
    keyboard.go()
