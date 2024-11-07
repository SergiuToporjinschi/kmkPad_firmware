from kmk.utils import Debug
from kmk.modules import Module
from usb_cdc import data
from custom.desktop_app.command import CommandHandler
import json

debug = Debug(__name__)

class DesktopConnection(Module):
    buffer: bytearray = bytearray()
    connectionStatus: bool = False
    commandHandler: CommandHandler = CommandHandler()
    
    # Move deviceInfo to configuration
    def __init__(self):
        pass

    def during_bootup(self, keyboard):
        try:
            data.timeout = 0
        except AttributeError:
            pass

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        pass

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        pass

    def before_hid_send(self, keyboard):
        line = self._readData()
        if line is None:
            return

        resp = self.commandHandler.Execute(keyboard, line.decode('utf-8'))
        self._writeAndFlash(resp)

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

    def deinit(self, keyboard):
        pass

    def _readData(self):
        # Serial.data isn't initialized.
        if not data:
            return
        
        if not data.connected:
            self.connectionStatus = False
            return
        
        if not self.connectionStatus:
            self.connectionStatus = True
            import custom.desktop_app.config as config
            c = config.ConfigHandler()
            self._writeAndFlash(json.dumps(c.identification))
            return

        # Nothing to parse.
        if data.in_waiting == 0:
            return

        self.buffer.extend(data.read())
        idx = self.buffer.find(b'\n')

        # No full command yet.
        if idx == -1:
            return
        
        # Split off command and evaluate.
        line = self.buffer[:idx]
        self.buffer = self.buffer[idx + 1 :]  # noqa: E203
        return line
    
    def _writeAndFlash(self, output: str):
        try:
            if output is not None:
                if not output.endswith('\n'):
                    output += '\n'

                data.write(output)
                data.flush()
                return
        except Exception as err:
            if debug.enabled:
                debug(f'error: {err}')
        return