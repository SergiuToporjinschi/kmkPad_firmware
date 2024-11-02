from kmk.keys import KC, Key, make_argumented_key
from kmk.extensions import Extension

class ScreenKey(Key):
    def __init__(self, line, message, key=None, **kwargs):
        super().__init__(**kwargs)
        self.line = line
        self.message = message
        self.key = key

class Sceen(Extension):
    def __init__(self):
        make_argumented_key(
            names=('SCREEN_LINE',),
            constructor=ScreenKey,
            on_press=None,
            on_release=None,
        )
        pass

    def on_runtime_enable(self, keyboard):
        raise NotImplementedError

    def on_runtime_disable(self, keyboard):
        raise NotImplementedError

    def during_bootup(self, keyboard):
        raise NotImplementedError

    def before_matrix_scan(self, keyboard):
        raise NotImplementedError

    def after_matrix_scan(self, keyboard):
        raise NotImplementedError

    def before_hid_send(self, keyboard):
        raise NotImplementedError

    def after_hid_send(self, keyboard):
        raise NotImplementedError

    def on_powersave_enable(self, keyboard):
        raise NotImplementedError

    def on_powersave_disable(self, keyboard):
        raise NotImplementedError

    def deinit(self, keyboard):
        pass
