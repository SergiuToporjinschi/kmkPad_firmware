from kmk.utils import Debug
from kmk.modules import Module
from kmk.kmk_keyboard import KMKKeyboard
import digitalio
import analogio

debug = Debug(__name__)


#key position in map 
class Joystick_key_position:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    RUN_MODIFIER = 4
    BUTTON = 5



class BaseJoystickKey:
    def __init__(self, travel_segments):
        self._button_state = True
        self._is_run = None
        self._button_held = None
        self._direction = None
        self.on_move_do = None
        self.on_button_do = None
        self._travel_segments = travel_segments

    def get_state(self):
        return {
            'direction': self._direction,
            'is_pressed': not self._button_state,
            'is_run': self._is_run,
        }

    def update_state(self):
        # debug(f'Axies: {self.pin_vrx.get_value()} {self.pin_vry.get_value()}') 
        # at this point 
        # Joystick fitted on the board has y horizontal axis and x vertical axis, but we consider y as vertical and x as horizontal 
        # following info is not refering to breadboard position but axis position
        # (0,0) is the center of the joystick (released)
        # if joystick is far UP Y value is between 0 and -5 (0,-5)
        # if joystick is far LEFT X value is between 0 and -5 (-5, 0)
        # if joystick is far DOWN Y value is between 0 and 5 (0, 5)
        # if joystick is far RIGHT X value is between 0 and 5 (5, 0)
        # b1=⬆️ 2=➡️ 3=⬇️ 4=⬅️ binary calculation first bit(from right to left) is up, second bit is right third bit is down fourth bit is left 
        xValue = self.pin_vrx.get_value()
        yValue = self.pin_vry.get_value()
        new_direction = ((yValue < 0) << 3) | (xValue > 0) << 2 | ((yValue > 0) << 1) | ((xValue < 0) << 0)

        # Rotate binary values to match joystick orientation (0, 90, 180, or 270 degrees)
        new_direction = self.rotate(new_direction, self.rotation)
        
        #if is far UP or DOWN or LEFT or RIGHT then add mofidifier key
        is_run = abs(yValue) == self._travel_segments or abs(xValue) == self._travel_segments

        if new_direction != self._direction or is_run != self._is_run: 
            self._direction = new_direction
            self._is_run = is_run
            if self.on_move_do is not None:
                self.on_move_do(self.get_state())
                
        # Button event
        self.button_event()

    def button_event(self):
        raise NotImplementedError('subclasses must override button_event()!')

    def rotate(self, binary_value, rotation):
        # Convert rotation degrees to number of bit rotations (0, 1, 2, or 3)
        #   00 ->   90 ->  180  ->  270 
        # 0110 -> 0011 -> 1001  -> 1100
        rotations = rotation // 90

        # Perform the rotation using bitwise operations for a 4-bit binary
        for _ in range(rotations):
            # Get the first bit (the most significant bit)
            first_bit = (binary_value >> 3) & 1
            
            # Shift the binary value to the left by 1 and wrap the first bit to the end
            binary_value = ((binary_value << 1) & 0b1111) | first_bit
        
        # Ensure we stay within 4 bits by masking any overflow
        return binary_value & 0b1111  # Mask with 0b1111 to keep only the lowest 4 bits

class GPIOJoystickKey(BaseJoystickKey):
    def __init__(
        self,
        pin_vrx,
        pin_vry,
        pin_button=None,
        rotation=0,
        travel_segments=5,
        button_pull=digitalio.Pull.UP,
    ):
        super().__init__(travel_segments)
        self.pin_vrx = JoystickKeyPin(pin_vrx, travel_segments)
        self.pin_vry = JoystickKeyPin(pin_vry, travel_segments)
        self.rotation = rotation

        if pin_button:
            self.pin_button = JoystickKeyPin(pin_button, button_type=True, pull=button_pull)
        else:
            self.pin_button = None

        if self.rotation not in (0, 90, 180, 270):
            debug("Invalid rotation value. Must be 0, 90, 180, or 270.")
            self.rotation = 0

    def button_event(self):
        if self.pin_button:
            new_button_state = self.pin_button.get_value()
            if new_button_state != self._button_state:
                self._button_state = new_button_state
                if self.on_button_do is not None:
                    self.on_button_do(self.get_state())

class JoystickKeyPin:
    def __init__(self, pin, travel_segments=5, button_type=False, pull=digitalio.Pull.UP):
        self.pin = pin
        self.button_type = button_type
        self.pull = pull
        self.travel_segments = travel_segments
        self.prepare_pin()

    def prepare_pin(self):
        if self.pin is not None and not self.button_type:
            if isinstance(self.pin, analogio.AnalogIn):
                self.io = self.pin
            else:
                self.io = analogio.AnalogIn(self.pin)
        elif self.pin is not None and self.button_type:
            if isinstance(self.pin, digitalio.DigitalInOut):
                self.io = self.pin
            else:
                self.io = digitalio.DigitalInOut(self.pin)
            self.io.direction = digitalio.Direction.INPUT
            self.io.pull = self.pull   
        else:
            self.io = None

    def get_value(self):
        io = self.io
        # 🕹️
        if not self.button_type: 
            result = self.filter_dead_zone(io.value)
        # ⌨️
        else:                   
            result = io.value
            if isinstance(self.pin, digitalio.DigitalInOut) and digitalio.Pull.UP != io.pull:
                result = not result
        return result
    
    def filter_dead_zone(self, value):
        in_min, in_max, out_min, out_max = (400, 65000, -self.travel_segments, self.travel_segments) # TODO: add calibration add 3.3v to ADC Ref pin ??!?! 
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min) if abs(value - 32768) > 500 else 0

class JoystickKeyHandler(Module): 
    def __init__(self):
        self.joysticks = []
        self.pins = None
        self.map = None

    def during_bootup(self, keyboard):
        if self.pins and self.map:
            for idx, jConfig in enumerate(self.pins):
                # debug(f'Joystick {idx} configured with {jConfig}')
                try:
                    new_joystick = GPIOJoystickKey(*jConfig)

                    new_joystick.on_move_do = lambda x, bound_idx=idx: self.on_move_do(
                        keyboard, bound_idx, x
                    )
                    new_joystick.on_button_do = (
                        lambda x, bound_idx=idx: self.on_button_do(
                            keyboard, bound_idx, x
                        )
                    )
                    self.joysticks.append(new_joystick)
                except Exception as e:
                    print(f"Error configuring joystick {idx}: {e}")

    def on_move_do(self, keyboard: KMKKeyboard, joystick_id, state):
        if self.map:
            layer_id = keyboard.active_layers[0]
            byte = state["direction"]
            b1 = (byte >> 3) & 1 # 1=⬆️
            b2 = (byte >> 2) & 1 # 2=➡️
            b3 = (byte >> 1) & 1 # 3=⬇️
            b4 = byte & 1        # 4=⬅️
            
            keyMap = self.map[layer_id][joystick_id]
            is_run = state['is_run']

            if is_run:
                keyboard.add_key(keyMap[Joystick_key_position.RUN_MODIFIER])
            else:
                keyboard.remove_key(keyMap[Joystick_key_position.RUN_MODIFIER])

            if b1: # 1=⬆️
                keyboard.add_key(keyMap[Joystick_key_position.UP])
            else:
                keyboard.remove_key(keyMap[Joystick_key_position.UP])
            
            if b2: # 2=➡️
                keyboard.add_key(keyMap[Joystick_key_position.RIGHT])
            else:
                keyboard.remove_key(keyMap[Joystick_key_position.RIGHT]) 
            
            if b3: # 3=⬇️
                keyboard.add_key(keyMap[Joystick_key_position.DOWN])
            else:
                keyboard.remove_key(keyMap[Joystick_key_position.DOWN])

            if b4: # 4=⬅️
                keyboard.add_key(keyMap[Joystick_key_position.LEFT])
            else:
                keyboard.remove_key(keyMap[Joystick_key_position.LEFT])

    def on_button_do(self, keyboard, joystick_id, state):
        if state['is_pressed'] is True:
            layer_id = keyboard.active_layers[0]
            key = self.map[layer_id][joystick_id][Joystick_key_position.BUTTON]
            keyboard.tap_key(key)
            
    def before_matrix_scan(self, keyboard):
        for joystick in self.joysticks:
            joystick.update_state()

    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

    def deinit(self, keyboard):
        pass