import json
import displayio
import terminalio
from adafruit_display_text import label

from kmk.kmk_keyboard import KMKKeyboard
from kmk.utils import Debug
from kmk.keys import ALL_ALPHAS,ALL_NUMBERS
from kmk.scanners import DiodeOrientation
# from .layer_descriptor import readLayerDescriptor
# from custom.desktop_app.layer_descriptor import readLayerDescriptor

debug = Debug(__name__)

class CommandHandler:
    commands: dict 

    def __init__(self):
        self.commands = {
            "keyboardActiveLayer": self._keyboardActiveLayer,
            "keyboardLayers": self._keyboardLayers,
            "changeActiveLayer": self._changeActiveLayer,
            "fetchAvailableBasicKeys": self._fetchAvailableBasicKeys,
            "getPinConfig": self._getPinConfig,
            "getLayerDescriptor": self._getLayerDescriptor,
        }
        pass

    def Execute(self, keyboard: KMKKeyboard, cmd: str) -> str:
        if cmd is None:
            return

        if debug.enabled:
            debug(f'cmd={cmd}' )

        cmd, args = self._extractArguments(cmd)
        if isinstance(self.commands, dict) and cmd in self.commands:
            return self.commands[cmd](keyboard, *args)
        else:
            return "error: Invalid command"
        

    def _extractArguments(self, cmd)->str:
        if ":" not in cmd:
            return cmd, ()
        cmd, args = cmd.split(":")
        return cmd, args.split(",")
        
########### Command Handlers ############ 
    def _changeActiveLayer(self, keyboard: KMKKeyboard, *args) -> str:
        debug(f'layerNumber={keyboard}')
        
        if len(args) != 1:
            return 'error: Invalid number of arguments'
        
        try:
            layerNumber = int(args[0])
            if layerNumber not in range(len(keyboard.keymap)):
                return 'error: Invalid Layer Number'

        except ValueError:
            return 'error: Invalid Layer Number'

        keyboard.active_layers = [layerNumber]

        return "success"
    
    def _keyboardActiveLayer(self, keyboard: KMKKeyboard, *args) -> str:
        return json.dumps(keyboard.active_layers)
    
    def _keyboardLayers(self, keyboard: KMKKeyboard, *args)->str:
        return json.dumps(keyboard.keymap)
    
    def _getPinConfig(self, keyboard: KMKKeyboard, *args)->str:
        diodeOrientation = "COL2ROW"
        if keyboard.diode_orientation == DiodeOrientation.ROW2COL:
            diodeOrientation = "ROW2COL"

        return json.dumps({
            "RowPins": [str(pin) for pin in keyboard.row_pins],
            "ColumnPins": [str(pin) for pin in keyboard.col_pins],
            "DiodeOrientation": diodeOrientation
        })
    
    def _getLayerDescriptor(self, keyboard: KMKKeyboard, *args)->str:
        return json.dumps(readLayerDescriptor())

    def _fetchAvailableBasicKeys(self, keyboard: KMKKeyboard, *args):
        debug(f'fetchAvailableBasicKeys')
        alpha = [{"Name": f"KC.{letter}", "Type": "KeyboardKey", "Code": 4 + i} for i, letter in enumerate(ALL_ALPHAS)]
        numbers = [{"Name": f"KC.N{n}", "Type": "KeyboardKey", "Code": 30 + i} for i, n in enumerate(ALL_NUMBERS)]
       
        numPadCodes = (
            (83, ('NUM_LOCK', 'NUMLOCK', 'NLCK')),
            (84, ('KP_SLASH', 'NUMPAD_SLASH', 'PSLS')),
            (85, ('KP_ASTERISK', 'NUMPAD_ASTERISK', 'PAST')),
            (86, ('KP_MINUS', 'NUMPAD_MINUS', 'PMNS')),
            (87, ('KP_PLUS', 'NUMPAD_PLUS', 'PPLS')),
            (88, ('KP_ENTER', 'NUMPAD_ENTER', 'PENT')),
            (89, ('KP_1', 'P1', 'NUMPAD_1')),
            (90, ('KP_2', 'P2', 'NUMPAD_2')),
            (91, ('KP_3', 'P3', 'NUMPAD_3')),
            (92, ('KP_4', 'P4', 'NUMPAD_4')),
            (93, ('KP_5', 'P5', 'NUMPAD_5')),
            (94, ('KP_6', 'P6', 'NUMPAD_6')),
            (95, ('KP_7', 'P7', 'NUMPAD_7')),
            (96, ('KP_8', 'P8', 'NUMPAD_8')),
            (97, ('KP_9', 'P9', 'NUMPAD_9')),
            (98, ('KP_0', 'P0', 'NUMPAD_0')),
            (99, ('KP_DOT', 'PDOT', 'NUMPAD_DOT')),
            (103, ('KP_EQUAL', 'PEQL', 'NUMPAD_EQUAL')),
            (133, ('KP_COMMA', 'PCMM', 'NUMPAD_COMMA')),
            # (134, ('KP_EQUAL_AS400', 'NUMPAD_EQUAL_AS400')),
        )
        numPadCodesDict = self._buildJsonFromCodTouples("KeyboardKey", numPadCodes)

        asciiCodes = (
            (40, ('ENTER', 'ENT', '\n')),
            (41, ('ESCAPE', 'ESC')),
            (42, ('BACKSPACE', 'BSPACE', 'BSPC', 'BKSP')),
            (43, ('TAB', '\t')),
            (44, ('SPACE', 'SPC', ' ')),
            (45, ('MINUS', 'MINS', '-')),
            (46, ('EQUAL', 'EQL', '=')),
            (47, ('LBRACKET', 'LBRC', '[')),
            (48, ('RBRACKET', 'RBRC', ']')),
            (49, ('BACKSLASH', 'BSLASH', 'BSLS', '\\')),
            (51, ('SEMICOLON', 'SCOLON', 'SCLN', ';')),
            (52, ('QUOTE', 'QUOT', "'")),
            (53, ('GRAVE', 'GRV', 'ZKHK', '`')),
            (54, ('COMMA', 'COMM', ',')),
            (55, ('DOT', '.')),
            (56, ('SLASH', 'SLSH', '/')),
        )
        asciiCodesDict = self._buildJsonFromCodTouples("KeyboardKey", asciiCodes)

        functionCodes = (
            (58, ('F1',)),
            (59, ('F2',)),
            (60, ('F3',)),
            (61, ('F4',)),
            (62, ('F5',)),
            (63, ('F6',)),
            (64, ('F7',)),
            (65, ('F8',)),
            (66, ('F9',)),
            (67, ('F10',)),
            (68, ('F11',)),
            (69, ('F12',)),
            (104, ('F13',)),
            (105, ('F14',)),
            (106, ('F15',)),
            (107, ('F16',)),
            (108, ('F17',)),
            (109, ('F18',)),
            (110, ('F19',)),
            (111, ('F20',)),
            (112, ('F21',)),
            (113, ('F22',)),
            (114, ('F23',)),
            (115, ('F24',)),
        )
        functionCodesDict = self._buildJsonFromCodTouples("KeyboardKey", functionCodes)

        navLockCodes = (
            (57, ('CAPS_LOCK', 'CAPSLOCK', 'CLCK', 'CAPS')),
            # FIXME: Investigate whether this key actually works, and
            #        uncomment when/if it does.
            # (130, ('LOCKING_CAPS', 'LCAP')),
            (70, ('PRINT_SCREEN', 'PSCREEN', 'PSCR')),
            (71, ('SCROLL_LOCK', 'SCROLLLOCK', 'SLCK')),
            # FIXME: Investigate whether this key actually works, and
            #        uncomment when/if it does.
            # (132, ('LOCKING_SCROLL', 'LSCRL')),
            (72, ('PAUSE', 'PAUS', 'BRK')),
            (73, ('INSERT', 'INS')),
            (74, ('HOME',)),
            (75, ('PGUP',)),
            (76, ('DELETE', 'DEL')),
            (77, ('END',)),
            (78, ('PGDOWN', 'PGDN')),
            (79, ('RIGHT', 'RGHT')),
            (80, ('LEFT',)),
            (81, ('DOWN',)),
            (82, ('UP',)),
        )
        navLockCodesDict = self._buildJsonFromCodTouples("KeyboardKey", navLockCodes)
        
        mods = (
            (0x01, ('LEFT_CONTROL', 'LCTRL', 'LCTL')),
            (0x02, ('LEFT_SHIFT', 'LSHIFT', 'LSFT')),
            (0x04, ('LEFT_ALT', 'LALT', 'LOPT')),
            (0x08, ('LEFT_SUPER', 'LGUI', 'LCMD', 'LWIN')),
            (0x10, ('RIGHT_CONTROL', 'RCTRL', 'RCTL')),
            (0x20, ('RIGHT_SHIFT', 'RSHIFT', 'RSFT')),
            (0x40, ('RIGHT_ALT', 'RALT', 'ROPT')),
            (0x80, ('RIGHT_SUPER', 'RGUI', 'RCMD', 'RWIN')),
            (0x07, ('MEH',)),
            (0x0F, ('HYPER', 'HYPR')),
        ) 
        modKeysDict = self._buildJsonFromCodTouples("ModifierKey",mods)
        
        shiftKeyCodes = (
            (30, ('EXCLAIM', 'EXLM', '!')),
            (31, ('AT', '@')),
            (32, ('HASH', 'POUND', '#')),
            (33, ('DOLLAR', 'DLR', '$')),
            (34, ('PERCENT', 'PERC', '%')),
            (35, ('CIRCUMFLEX', 'CIRC', '^')),
            (36, ('AMPERSAND', 'AMPR', '&')),
            (37, ('ASTERISK', 'ASTR', '*')),
            (38, ('LEFT_PAREN', 'LPRN', '(')),
            (39, ('RIGHT_PAREN', 'RPRN', ')')),
            (45, ('UNDERSCORE', 'UNDS', '_')),
            (46, ('PLUS', '+')),
            (47, ('LEFT_CURLY_BRACE', 'LCBR', '{')),
            (48, ('RIGHT_CURLY_BRACE', 'RCBR', '}')),
            (49, ('PIPE', '|')),
            (51, ('COLON', 'COLN', ':')),
            (52, ('DOUBLE_QUOTE', 'DQUO', 'DQT', '"')),
            (53, ('TILDE', 'TILD', '~')),
            (54, ('LEFT_ANGLE_BRACKET', 'LABK', '<')),
            (55, ('RIGHT_ANGLE_BRACKET', 'RABK', '>')),
            (56, ('QUESTION', 'QUES', '?')),
        )
        shiftKeyCodesDict = self._buildJsonFromCodTouples("ModifierKey",shiftKeyCodes)

        firmWareKeys = (
            (None,('BLE_REFRESH','BLE_RF')),
            (None,('BLE_DISCONNECT','BLE_DC')),
            (None,('BOOTLOADER','BTLD')),
            (None,('DEBUG', 'DBG')),
            (None,('HID_SWITCH', 'HID')),
            (None,('RELOAD', 'RLD')),
            (None,('RESET',)),
            (None,('ANY',)),
        )
        firmwareKeyDict = self._buildJsonFromCodTouples("CollableKey", firmWareKeys)

        specialKeys = (
             (None,('NO', 'XXXXXXX')),
             (None,('TRANSPARENT', 'TRNS')),
        )
        specialKeysDict = self._buildJsonFromCodTouples("CollableKey", specialKeys)

        return json.dumps(
            alpha+
            numbers+
            numPadCodesDict+
            shiftKeyCodesDict+
            asciiCodesDict+
            functionCodesDict+
            modKeysDict+
            navLockCodesDict+
            firmwareKeyDict+
            specialKeysDict)
    
    def _buildJsonFromCodTouples(self, typeKey, touples) -> dict:
        jsonDict =[]
        for code, names in touples:
            template = {"Name": f"{names[0]}", "Type": f"{typeKey}"}
            if code is not None:
                template["Code"] = code
            for name in names[1:]:
                if "Aliases" not in template:
                    template["Aliases"] = []
                template["Aliases"].append(f"KC.{name}")
            jsonDict.append(template)

        return jsonDict










########### Display Handlers ############ 
    def _updateDisplay(self, keyboard):
        if keyboard.extensions[0]:
            self._displayLayer(keyboard)
    def _displayLayer(self, keyboard):
        dispExt = keyboard.extensions[0]

        if dispExt:
            # dispExt.render(1)
            dispExt.display.wake()
            scr = displayio.Group()
            scr.append(
                    label.Label(
                        terminalio.FONT,
                        text="Active layer:" + str(keyboard.active_layers[0]),
                        color=0xFFFFFF,
                        background_color=0x000000,
                        anchor_point= (0.0, 0.0),
                        anchored_position=(0, 0),
                        label_direction="LTR",
                        line_spacing=0.75,
                        padding_left=1,
                    )
            )
            dispExt.display.root_group = scr
            # dispExt.render(keyboard.active_layers[0])

        pass


