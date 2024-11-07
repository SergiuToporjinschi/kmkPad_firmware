from kmk.keys import make_argumented_key, Key
from kmk.utils import Debug
from kmk.extensions.display import Display
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font
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
        self._layer_names = None
        self._layer_value = None
        self._initialized = False
        self._title = None
        self._version = None
        self._create_keys()
       

    def __setitem__(self, name, value):
        super().__setattr__(name, value)

    @property
    def config(self):
        return None

    @config.setter
    def config(self, config:ConfigHandler):
        self._title = config.identification_name
        self._version = config.identification_version
        nr_layers = config.layers_get_count()

        self._layer_names = [int] * config.layers_get_count()
        for index in range(nr_layers):
            self._layer_names[index] = config.layers_get_by_index(index)['name']
        
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

    def render(self, active_layer):
        if not self._initialized:
            _layer_label = label.Label(Font.GetFont(Font.ArialBold15), text="Layer", color=0xFFFFFF, x=75, y=5, anchor_point=(0.0, 0.0))
            self._layer_value = label.Label(Font.GetFont(Font.ArialBold10), text=self._layer_names[active_layer], color=0xFFFFFF, x=75, y=24, anchor_point=(0.0, 0.0))
            
            self._info_line_1 = label.Label(Font.GetFont(Font.ArialBold10), text=" "*20, color=0xFFFFFF, x=0, y=44, anchor_point=(0.0, 0.0))
            self._info_line_2 = label.Label(Font.GetFont(Font.ArialBold10), text=" "*20, color=0xFFFFFF, x=0, y=56, anchor_point=(0.0, 0.0))
            self.display.root_group = displayio.Group()
            self.display.root_group.append(label.Label(Font.GetFont(Font.ArialBold15), text=self._title, color=0xFFFFFF, x=0, y=5, anchor_point=(0.0, 0.0)))
            self.display.root_group.append( label.Label(Font.GetFont(Font.ArialBold8), text=self._version, color=0xFFFFFF, x=0, y=24, anchor_point=(0.0, 0.0)))
            self.display.root_group.append(Line(70, 0, 70, 32, 0xFFFFFF))
            self.display.root_group.append(_layer_label)
            self.display.root_group.append(self._layer_value)
            self.display.root_group.append(Line(0, 32, 128, 32, 0xFFFFFF))
            self.display.root_group.append(self._info_line_1)
            self.display.root_group.append(self._info_line_2)
            self._initialized = True
        else:
            self._layer_value.text = self._layer_names[active_layer]

    def on_runtime_enable(self, keyboard):
        super().on_runtime_enable(keyboard)

    def on_runtime_disable(self, keyboard):
        super().on_runtime_disable(keyboard)

    def during_bootup(self, keyboard):
        super().during_bootup(keyboard)


    def before_matrix_scan(self, keyboard):
        super().before_matrix_scan(keyboard)

    def after_matrix_scan(self, keyboard): super().after_matrix_scan(keyboard)
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): super().on_powersave_enable(keyboard)
    def on_powersave_disable(self, keyboard): super().on_powersave_disable(keyboard)
    def deinit(self, keyboard): super().deinit(keyboard)
