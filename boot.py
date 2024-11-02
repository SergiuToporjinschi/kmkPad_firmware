from kmk.bootcfg import bootcfg
import digitalio


bootcfg(
    sense= digitalio.DigitalInOut,
    source=  None,
    autoreload= True,
    boot_device=0,
    cdc_console=True,
    cdc_data=True,
    consumer_control= True,
    keyboard= True,
    midi= True,
    mouse = True,
    nkro = False,
    pan = False,
    storage = True,
    # usb_id= ('6001', '1000'),
)
import supervisor
supervisor.set_usb_identification("Pad","kmkPad", 0x6001, 0x1000)

# import board
# import storage
# switch = digitalio.DigitalInOut(board.GP2)
# switch.direction = digitalio.Direction.INPUT
# switch.pull = digitalio.Pull.UP

# # If the switch pin is connected to ground CircuitPython can write to the drive
# storage.remount("/", readonly=switch.value)