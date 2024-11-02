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
# from custom_extensions.joystick import Joystick
from custom.module.joystick_key_press import JoystickHandler  

joystick = JoystickHandler()
joystick.pins = ((board.GP27, board.GP26, board.GP22, 90), )
# joystick.map = [((KC.NO, KC.NO, KC.NO, KC.NO, KC.NO),) ] #⬆️⬇️⬅️➡️ 
joystick.map = [((KC.W, KC.S, KC.A, KC.D, KC.X),) ] #⬆️⬇️⬅️➡️ 

keyboard = KMKKeyboard()
 
keyboard.col_pins = (board.GP13, board.GP12, board.GP11, board.GP10, board.GP9,)
keyboard.row_pins = (board.GP15, board.GP14)
keyboard.diode_orientation = DiodeOrientation.ROW2COL
keyboard.debug_enabled = False  

encoder_handler = EncoderHandler()
desktopCom = DesktopConnection()
keyboardLayers = Layers()
mediaKey = MediaKeys()
macros = Macros()
holdtap = HoldTap()

ssd1306Inst = SH1106_I2C(busio.I2C(board.GP21, board.GP20))
layerChanged = TextEntry(layer=1,text="Layer changed!")

display = Display(display=ssd1306Inst, width=128, height=64,entries=[], brightness=0.5,
        dim_time = 2,
        dim_target = 0.1,
        brightness_step = 0.01,
        off_time= 0,
        flip = False,
        powersave_dim_time=2,
        powersave_dim_target=0.01,
        powersave_off_time=20,
        )

keyboard.debug_enabled = True

keyboard.extensions = [display, mediaKey]
keyboard.modules = [joystick, encoder_handler, macros, keyboardLayers, desktopCom, holdtap]

ctrl_Shift_F5 = KC.MACRO(Press(KC.LCTL), Press(KC.LSFT), Tap(KC.F5), Release(KC.LSFT), Release(KC.LCTL))
s = KC.MACRO("Wow, KMK is awesome!")

encoder_handler.pins = ((board.GP17, board.GP16, board.GP18, False,1), )

keyboard.keymap = [
		[
            KC.N1,	 KC.W,	  KC.N3,    KC.N4,  KC.N5,
		    KC.A,   KC.S,   KC.D,    KC.F7,  KC.F8,
        ],
		# [
        #     KC.get('F5'),	 KC.get('w'),	  KC.E,    KC.R,  KC.RLD,
		#     ctrl_Shift_F5,   KC.LCTRL(KC.LSFT(KC.F5)),    KC.D,    KC.F,  KC.RESET,
        # ],
        [
            KC.get('F5'),	 KC.N2,	  KC.N3,    KC.N4,  KC.N5,
            KC.LCTRL(KC.LSFT(KC.F5)),	 KC.N7,	  KC.N8,    KC.N9,  KC.N0,
        ]
] 
encoder_handler.map = [((KC.VOLU, KC.VOLD, KC.MUTE),) ]

print(f'{keyboard.keymap[0][0].code}')


display.entries = [
        TextEntry(text="Basic", x=0, y=0, layer=0),
        TextEntry(text="Row: 1" , x=0, y=12),
        TextEntry(text="Layer = 1, Row 3", x=0, y=24),
        TextEntry(text="Layer = 1, Row 4", x=0, y=36),
        TextEntry(text="Layer = 1, Row 5", x=0, y=48),
]

if __name__ == '__main__':
    keyboard.go()
