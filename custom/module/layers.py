from kmk.modules.layers import Layers, LayerKey
from kmk.keys import KC, Key, make_argumented_key
from kmk.utils import Debug

debug = Debug(__name__)

class Layers(Layers):
    '''
    if this PR https://github.com/KMKfw/kmk_firmware/pull/1043 is merged then you can remove this 
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        make_argumented_key(
            names=('TGS',),
            constructor=LayerKey,
            on_press=self._tgs_pressed,
        )

    def _tgs_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Changes the order of layers in the active_layers list
        '''
        # See mo_released for implementation details around this
        if key.layer == 'UP':
        # Move each element to the left with one position
            keyboard.active_layers = keyboard.active_layers[1:] + [keyboard.active_layers[0]]
        elif key.layer == 'DOWN':
            # Move each element to the right with one position
            keyboard.active_layers = [keyboard.active_layers[-1]] + keyboard.active_layers[:-1]
        else:
            raise ValueError("Direction must be 'up' or 'down'")
        self._print_debug(keyboard)