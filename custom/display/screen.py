from kmk.keys import Key, make_key
from kmk.extensions import Extension
from kmk.utils import Debug
from kmk.extensions.display import Display
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font
from custom.desktop_app.layer_descriptor import readLayerDescriptor
import terminalio
import displayio

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
            ('SK_INF1',),
            on_press=self.on_screen_info_line1_press,
            on_release=self.on_screen_info_line1_release,
        ),
        make_key(
            ('SK_INF2',),
            on_press=self.on_screen_info_line2_press,
            on_release=self.on_screen_info_line2_release,
        ),
        self._bild_screen()
        self._layer_descriptor = readLayerDescriptor()
        pass

    def on_screen_info_line1_press(self, key, keyboard): pass
    def on_screen_info_line1_release(self, key, keyboard): pass
    def on_screen_info_line2_press(self, key, keyboard): pass
    def on_screen_info_line2_release(self, key, keyboard): pass

    def _bild_screen(self):
        
        self._name_title = label.Label(Font.GetFont(Font.ArialBold15), text="DEV Pad", color=0xFFFFFF, x=0, y=5, anchor_point=(0.0, 0.0)) #TODO get value from config 
        self._name_title_version = label.Label(Font.GetFont(Font.ArialBold8), text="V 0.01", color=0xFFFFFF, x=0, y=24, anchor_point=(0.0, 0.0)) #TODO get value from config
        self._layer_label = label.Label(Font.GetFont(Font.ArialBold15), text="Layer", color=0xFFFFFF, x=75, y=5, anchored_point=(0.0, 0.0))
        
        self._layer_value = label.Label(Font.GetFont(Font.ArialBold10), text=" "*7, color=0xFFFFFF, x=75, y=24, anchored_point=(0.0, 0.0))
        
        self._screen_group = displayio.Group()
        self._screen_group.append(self._name_title)
        self._screen_group.append(self._name_title_version)
        self._screen_group.append(Line(70, 0, 70, 32, 0xFFFFFF))
        self._screen_group.append(self._layer_label)
        self._screen_group.append(self._layer_value)
        self._screen_group.append(Line(0, 32, 128, 32, 0xFFFFFF))
        # palette = displayio.Palette(2)
        # palette[0] = 0x000000
        # palette[1] = 0xffffff
        
        # bmp = displayio.OnDiskBitmap("fonts/layer4.bmp")
        # debug("bmp.width: " + str(bmp.width))
        # tl = displayio.TileGrid(bmp, pixel_shader=bmp.pixel_shader, x=0, y=34, width=1, height=1, tile_width=bmp.width, tile_height=bmp.height)
        # self._screen_group.append(tl)

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
        if keyboard is not None:
            self._current_layer = keyboard.active_layers[0]
        pass

    def before_matrix_scan(self, keyboard):
        if self._display is not None and self._display.display.root_group != self._screen_group:
            self._display.display.root_group = self._screen_group
        
        # self._layer_value.text = f"{keyboard.active_layers[0]}" #TODO get value from config 
        if self._current_layer != keyboard.active_layers[0]:
            self._current_layer = keyboard.active_layers[0]
            debug(f'{keyboard.active_layers[0]}')
            for layer in self._layer_descriptor:
                if layer['Index'] == keyboard.active_layers[0]:
                    self._layer_value.text = layer['Name']
                    break
        # debug(f"Layer: {self._layer_descriptor}")
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
