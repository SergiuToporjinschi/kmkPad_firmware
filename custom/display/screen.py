from kmk.keys import KC, Key, make_argumented_key, make_key
from kmk.extensions import Extension
from kmk.utils import Debug
from kmk.extensions.display import Display

debug = Debug(__name__)

class ScreenKey(Key):
    def __init__(self, line, message, key=None, **kwargs):
        super().__init__(**kwargs)
        self.line = line
        self.message = message
        self.key = key
class Screen(Extension):
    def __init__(self):
        debug("Screen extension initialized")
        make_key(
            ('SK_LINE',),
            on_press=self.on_screen_line_press,
            on_release=self.on_screen_line_release,
        ),
        # make_argumented_key(
        #     names=('SCREEN_LINE',),
        #     constructor=ScreenKey,
        #     on_press=self.on_scree_line_press,
        #     on_release=self.on_scree_line_release,
        # )
        pass
    def on_screen_line_press(self, key, keyboard, a, b):
        debug(f"Screen key pressed: {key} {keyboard}")
        # keyboard.display.entries[key.line] = key.message
        # if key.key is not None:
        #     keyboard.tap_key(key)
    def on_screen_line_release(self, key, keyboard, a, b):
        debug(f"Screen key pressed: {key} {keyboard.extensions}")
        # for  extension in keyboard.extensions:
        #     if isinstance(extension, Display):
        #         extension.on_screen_line_release(key, keyboard)
        # keyboard.display.entries[key.line] = key.message
        # if key.key is not None:
        #     keyboard.tap_key(key)
                             
    def on_runtime_enable(self, keyboard):
        raise NotImplementedError

    def on_runtime_disable(self, keyboard):
        raise NotImplementedError

    def during_bootup(self, keyboard):
        # raise NotImplementedError
        pass
    def before_matrix_scan(self, keyboard):
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
