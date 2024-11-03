from kmk.keys import Key, make_key
from kmk.extensions import Extension
from kmk.utils import Debug
from kmk.extensions.display import Display
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect   
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font

import terminalio
import displayio

debug = Debug(__name__)


class Fonts:
    arial_8 = "fonts/arial-75-8.bdf"

class ScreenKey(Key):
    def __init__(self, line, message, key=None, **kwargs):
        super().__init__(**kwargs)
        self.line = line
        self.message = message
        self.key = key

class Screen(Extension):
    _display:Display = None

    def __init__(self):
        debug("Screen extension initialized")
        self._lastLayer = None
        self._display = None
        make_key(
            ('SK_LINE',),
            on_press=self.on_screen_line_press,
            on_release=self.on_screen_line_release,
        ),

        self._bild_screen()
        # make_argumented_key(
        #     names=('SCREEN_LINE',),
        #     constructor=ScreenKey,
        #     on_press=self.on_scree_line_press,
        #     on_release=self.on_scree_line_release,
        # )
        pass
    def on_screen_line_press(self, key, keyboard, a, b):
        if self._name_title is not None:
            self._name_title.text = "Pushed"
        # keyboard.display.entries[key.line] = key.message
        # if key.key is not None:
        #     keyboard.tap_key(key)
    def on_screen_line_release(self, key, keyboard, a, b):
        if self._name_title is not None:
            self._name_title.text = "Released"
        pass
        # debug(f"Screen key pressed: {key} {keyboard.extensions}")
        # for  extension in keyboard.extensions:
        #     if isinstance(extension, Display):
        #         extension.on_screen_line_release(key, keyboard)
        # keyboard.display.entries[key.line] = key.message
        # if key.key is not None:
        #     keyboard.tap_key(key)
    def _bild_screen(self):
        # aria = bitmap_font.load_font(Fonts.arial_8)
        self._name_title = label.Label(terminalio.FONT, text="DEV Pad", color=0xFFFFFF, x=0, y=10, anchored_point=(0.0, 0.0))
        self._layer_name = label.Label(terminalio.FONT, text=" "*10, color=0xFFFFFF, x=20, y=10, anchored_point=(0.0, 0.0))
        middleLine = Line(0, 15, 128, 15, 0xFFFFFF)
        self._screen_group = displayio.Group()
        self._screen_group.append(self._name_title)
        self._screen_group.append(middleLine)

    def on_runtime_enable(self, keyboard):
        debug("Screen extension enabled")

        # raise NotImplementedError 

    def on_runtime_disable(self, keyboard):
        debug("Screen extension disabled")
        # raise NotImplementedError

    def during_bootup(self, keyboard):
        # raise NotImplementedError
        if self._display is None:
            for extension in keyboard.extensions:
                if isinstance(extension, Display):
                    debug("Screen extension found")
                    self._display = extension
                    break
        pass
    def before_matrix_scan(self, keyboard):
        if self._display is not None:
            self._display.display.root_group = self._screen_group
        pass # raise NotImplementedError

    def after_matrix_scan(self, keyboard):
        pass # raise NotImplementedError

    def before_hid_send(self, keyboard):
        pass #raise NotImplementedError

    def after_hid_send(self, keyboard):
         pass #raise NotImplementedError

    def on_powersave_enable(self, keyboard):
        raise NotImplementedError

    def on_powersave_disable(self, keyboard):
        raise NotImplementedError

    def deinit(self, keyboard):
        pass
