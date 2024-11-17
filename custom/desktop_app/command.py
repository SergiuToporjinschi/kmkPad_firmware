from kmk.kmk_keyboard import KMKKeyboard


class CommandHandler:
    commands: dict 

    def __init__(self):
        self.commands = {
            "keyboardActiveLayer": self._keyboardActiveLayer,
            "keyboardLayers": self._keyboardLayers,
            "changeActiveLayer": self._changeActiveLayer,
            "getConfig": self._getConfig,
        }
        pass

    def Execute(self, keyboard: KMKKeyboard, cmd: str) -> str:
        if cmd is None:
            return

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
    
    def _getConfig(self, keyboard: KMKKeyboard, *args)->str:
        from custom.desktop_app.config import readConfig
        return readConfig()
