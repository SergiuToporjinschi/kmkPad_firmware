import json
import board 
from kmk.keys import KC
from kmk.utils import Debug
from kmk.keys import KeyboardKey, ConsumerKey, Key
debug = Debug(__name__)

config = None

class ConfigHandler:
    _nr_keyboard_layers = None
    _no_of_keys = None
    
    def __init__(self):
        try:
            with open('/config.json') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            if debug.enabled:
                debug('Config file not found')
            self.config = {}
        except json.JSONDecodeError:
            if debug.enabled:
                debug('Error decoding config file')
            self.config = {}
        if debug.enabled:
            debug('Config loaded')
        
    @property
    def debug_enabled(self) -> bool:
        return self.config.get('debug', False)
    
    @property
    def title(self) -> str:
        return self.config['title']

    @property
    def version(self) -> str:
        return self.config['version']
    
    #----------------------------------------------------keyboard
    @property
    def keyboard_GPIO_pin_rows(self) -> tuple:
        rowPins = self._build_gpios(self.config['keyboard']['gpioPinRows'])
        self._no_of_keys = len(rowPins) * len(self.config['keyboard']['gpioPinCols'])
        return rowPins

    @property
    def keyboard_GPIO_pin_cols(self) -> tuple:
        colPins = self._build_gpios(self.config['keyboard']['gpioPinCols'])
        self._no_of_keys = len(colPins) * len(self.config['keyboard']['gpioPinRows'])
        return colPins

    @property
    def keyboard_diode_orientation(self) -> int: 
        ''' 
        1 = DiodeOrientation.ROW2COL = ROWS; 
        0 = DiodeOrientation.COL2ROW = COLUMNS 
        '''
        return self.config['keyboard']['diodeOrientation']
    
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
    def encoder_GPIO_pins(self) -> tuple:
        return self._build_gpios(self.config['encoders'][0]['gpioPins'])
    
    def _build_gpios(self, gpio_pins: list) -> tuple:
        outPut = ()
        for boarGPIO in gpio_pins:
            gpio = {}
            exec(f'gpio = board.{boarGPIO}', {'board': board}, gpio)
            outPut += (gpio.get('gpio'),)
        return outPut

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
    def joystickKey_enabled(self) -> bool:
        return self.config['joystickKeys'][0]['enabled']
    
    @property
    def joystickKey_rotation(self) -> list:    
        return self.config['joystickKeys'][0]['rotation']
    
    @property
    def joystickKey_travel_segments(self) -> list:
        return self.config['joystickKeys'][0]['travelSegments']
    
    @property
    def joystickKey_GPIO_pins(self) -> tuple:
        return self._build_gpios(self.config['joystickKeys'][0]['gpioPins'])

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
        ret_layers = [None] * len(self.config['keyboard']['layers'])
        for layer in self.config['keyboard']['layers']:
            ret_layers[layer['index']] = self._build_key_map(layer['map'], self._no_of_keys)

        self._nr_keyboard_layers = len(ret_layers)
        return ret_layers
    
    @property
    def layers_encoders_maps(self) -> list:
        enc_layers =  [None] * self._nr_keyboard_layers
        for i in range(self._nr_keyboard_layers):
            layer = self._find_layer_by_index(self.config['encoders'][0]['layers'], i)
            if layer is not None:
                enc_layers[i] = [self._build_key_map(layer['map'], 3)]
            else:
                enc_layers[i] = [[KC.TRNS, KC.TRNS, KC.TRNS]]
        
        return enc_layers

    @property   
    def layers_joystickKeys_maps(self) -> list:
        _joystickKey_layers =  [None] * self._nr_keyboard_layers
        for i in range(self._nr_keyboard_layers):
            layer = self._find_layer_by_index(self.config['joystickKeys'][0]['layers'], i)
            if layer is not None:
                _joystickKey_layers[i] = [self._build_key_map(layer['map'], 6)]
            else:
                _joystickKey_layers[i] = [[KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS]]
        return _joystickKey_layers

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