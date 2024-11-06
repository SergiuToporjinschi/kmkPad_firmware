import json
from kmk.keys import KC
from kmk.utils import Debug
from kmk.keys import KeyboardKey, ConsumerKey, Key
debug = Debug(__name__)

config = None

class ConfigHandler:
    _instance = None
    _keyboard_layers = None
    _nr_keyboard_layers = None
    _encoder_layers = None  
    _joystickKey_layers = None  

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigHandler, cls).__new__(cls)
        
        global config
        config = cls._instance
        return cls._instance

    def __init__(self, no_of_keys: int = None):
        if not hasattr(self, 'initialized'):
            self._no_of_keys = no_of_keys
            self.initialized = True
    
    def load_config(self):
        self.config = self._read_config()
        if debug.enabled:
            debug('Config loaded')

    def _read_config(self):
        try:
            with open('/config.json') as f:
                return json.load(f)
        except FileNotFoundError:
            if debug.enabled:
                debug('Config file not found')
            return {}
        except json.JSONDecodeError:
            if debug.enabled:
                debug('Error decoding config file')
            return {}
        
    @property
    def debug_enabled(self) -> bool:
        return self.config.get('debug', False)
    
    @property
    def title(self) -> str:
        return self.config['title']

    @property
    def version(self) -> str:
        return self.config['version']
    
    #----------------------------------------------------screen
    @property   
    def screen_enabled(self) -> bool:
        return self.config['screen']['enabled']

    @property
    def screen_width(self) -> int:
        return self.config['screen']['width']
    
    @property
    def screen_height(self) -> int:
        return self.config['screen']['height']

    @property
    def screen_brightness(self) -> float:
        return self.config['screen']['brightness']

    @property
    def screen_brightness_step(self) -> float:
        return self.config['screen']['brightnessStep']

    @property
    def screen_flip(self) -> bool:
        return self.config['screen']['flip']
    
    @property
    def screen_dim_timeout(self) -> int:
        return self.config['screen']['dimTimeout']
    
    @property
    def screen_dim_target(self) -> float:
        return self.config['screen']['dimTarget']

    @property
    def screen_off_time(self) -> int:
        return self.config['screen']['offTime']
   
    #----------------------------------------------------encoder
    @property
    def encoder_enabled(self) -> int:
        return self.config['encoders'][0]['enabled']

    @property
    def encoder_reversed(self) -> bool:
        return self.config['encoders'][0]['reversed']
    
    @property
    def encoder_divisor(self) -> int:
        return self.config['encoders'][0]['divisor']

    #----------------------------------------------------joystick
    @property
    def joystick_enabled(self) -> bool:
        return self.config['joystickKeys'][0]['enabled']
    
    @property
    def joystick_rotation(self) -> list:    
        return self.config['joystickKeys'][0]['rotation']
    
    @property
    def joystick_travel_segments(self) -> list:
        return self.config['joystickKeys'][0]['travelSegments']

    #----------------------------------------------------layers
    def layers_get_by_index(self, index: int) -> dict:
        for layer in self.config['keyboard']['layers']:
            if layer['index'] == index:
                return layer
        return None

    @property
    def media_keys_enabled(self) -> bool:
        return True

    @property
    def macro_keys_enabled(self) -> bool:
        return True

    @property
    def layers_key_maps(self) -> list:
        if self._keyboard_layers is not None:
            return self._keyboard_layers
        
        ret_layers = [None] * len(self.config['keyboard']['layers'])
        for layer in self.config['keyboard']['layers']:
            ret_layers[layer['index']] = self._build_key_map(layer['map'], self._no_of_keys)

        self._keyboard_layers = ret_layers
        self._nr_keyboard_layers = len(ret_layers)
        return ret_layers
    
    @property
    def layers_encoders_maps(self) -> list:
        if self._encoder_layers is not None:
            return self._encoder_layers
        
        enc_layers =  [None] * self._nr_keyboard_layers
        for i in range(self._nr_keyboard_layers):
            layer = self._find_layer_by_index(self.config['encoders'][0]['layers'], i)
            if layer is not None:
                enc_layers[i] = [self._build_key_map(layer['map'], 3)]
            else:
                enc_layers[i] = [[KC.TRNS, KC.TRNS, KC.TRNS]]
        
        self._encoder_layers = enc_layers
        return enc_layers

    @property   
    def layers_joystick_keys_maps(self) -> list:
        self._joystickKey_layers =  [None] * self._nr_keyboard_layers
        for i in range(self._nr_keyboard_layers):
            layer = self._find_layer_by_index(self.config['joystickKeys'][0]['layers'], i)
            if layer is not None:
                self._joystickKey_layers[i] = self._build_key_map(layer['map'], 6)
            else:
                self._joystickKey_layers[i] = [KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS]
        pass

    def _build_key_map(self, key_map: list, no_of_keys: int):
        ret_key_map = [] 
        for i in range(no_of_keys):
            if i < len(key_map):
                key = self._build_key(key_map[i])
                ret_key_map.append(key)
            else:
                ret_key_map.append(KC.NO)
        return ret_key_map
    
    def _build_key(self, keyString : str) -> KeyboardKey:
        local_vars = {}
        global_vars = {
            'KC': KC,
        }
        exec(f'key = {keyString}', global_vars, local_vars) # I don't like this but is the only way to get the key object from a string
        key = local_vars.get('key')
        if isinstance(key, (KeyboardKey, ConsumerKey, Key)):
            return key

        return KC.NO

    def _find_layer_by_index(self, layers: list, index: int) -> dict:
        for layer in layers:
            if layer['index'] == index:
                return layer
        return None