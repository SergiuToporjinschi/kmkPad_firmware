from kmk.keys import make_key,make_argumented_key, Key
from kmk.utils import Debug
from kmk.extensions.display import Display
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font
# from custom.desktop_app.layer_descriptor import readLayerDescriptor
import terminalio
import displayio
from custom.desktop_app.config import ConfigHandler

debug = Debug(__name__)

class Font:
    ArialBold15 = "/fonts/Arial-BoldMT-15.bdf"
    ArialBold8 = "/fonts/Arial-BoldMT-8.bdf"
    ArialBold10 = "/fonts/Arial-BoldMT-10.bdf"

    @staticmethod
    def GetFont(font):
        if font is not None:
            return bitmap_font.load_font(font)
        return terminalio.FONT
    
class ScreenKey(Key):
    def __init__(self, line, message,  **kwargs):
        super().__init__(**kwargs)
        self.line = line
        self.message = message

class Screen(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        debug("Screen extension initialized")
        self._lastLayer = None
        self._config = ConfigHandler()
        self._create_keys()
        self._bild_screen()

    def _create_keys(self):
        make_argumented_key(
            names=('SK_INF',),
            constructor=ScreenKey,
            on_press=self.on_screen_info_line_press,
            on_release=self.on_screen_info_line_release,
        )

    def on_screen_info_line_press(self, key, keyboard, *args, **kwargs): 
        if key.line == 1:
            self._info_line_1.text = key.message
        if key.line == 2:
            self._info_line_2.text = key.message

    def on_screen_info_line_release(self, key, keyboard, *args, **kwargs): 
        if key.line == 1:
            self._info_line_1.text = ""
        if key.line == 2:
            self._info_line_2.text = ""


    def _bild_screen(self):
        _name_title = label.Label(Font.GetFont(Font.ArialBold15), text=self._config.title, color=0xFFFFFF, x=0, y=5, anchor_point=(0.0, 0.0))
        _name_title_version = label.Label(Font.GetFont(Font.ArialBold8), text=self._config.version, color=0xFFFFFF, x=0, y=24, anchor_point=(0.0, 0.0))
        _layer_label = label.Label(Font.GetFont(Font.ArialBold15), text="Layer", color=0xFFFFFF, x=75, y=5, anchor_point=(0.0, 0.0))
        self._layer_value = label.Label(Font.GetFont(Font.ArialBold10), text=" "*7, color=0xFFFFFF, x=75, y=24, anchor_point=(0.0, 0.0))
        
        self._info_line_1 = label.Label(Font.GetFont(Font.ArialBold10), text=" "*20, color=0xFFFFFF, x=0, y=44, anchor_point=(0.0, 0.0))
        self._info_line_2 = label.Label(Font.GetFont(Font.ArialBold10), text=" "*20, color=0xFFFFFF, x=0, y=56, anchor_point=(0.0, 0.0))

        self._screen_group = displayio.Group()
        self._screen_group.append(_name_title)
        self._screen_group.append(_name_title_version)
        self._screen_group.append(Line(70, 0, 70, 32, 0xFFFFFF))
        self._screen_group.append(_layer_label)
        self._screen_group.append(self._layer_value)
        self._screen_group.append(Line(0, 32, 128, 32, 0xFFFFFF))
        self._screen_group.append(self._info_line_1)
        self._screen_group.append(self._info_line_2)


    def on_runtime_enable(self, keyboard):
        super().on_runtime_enable(keyboard)

    def on_runtime_disable(self, keyboard):
        super().on_runtime_disable(keyboard)

    def during_bootup(self, keyboard):
        super().during_bootup(keyboard)
        if keyboard is not None:
            self._current_layer = keyboard.active_layers[0]
            layer_config = self._config.layers_get_by_index(self._current_layer)
            self._layer_value.text = layer_config['name']

    def before_matrix_scan(self, keyboard):
        super().before_matrix_scan(keyboard)
        if self.display is not None and self.display.root_group != self._screen_group:
            self.display.root_group = self._screen_group

        if self._current_layer != keyboard.active_layers[0]:
            self._current_layer = keyboard.active_layers[0]
            layer_config = self._config.layers_get_by_index(self._current_layer)
            self._layer_value.text = layer_config['name']

    def after_matrix_scan(self, keyboard): super().after_matrix_scan(keyboard)
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): super().on_powersave_enable(keyboard)
    def on_powersave_disable(self, keyboard): super().on_powersave_disable(keyboard)
    def deinit(self, keyboard): super().deinit(keyboard)
