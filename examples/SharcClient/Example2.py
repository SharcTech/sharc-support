#from examples.SharcClient.Client import Client
from Client import Client

from textual.widget import Widget
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Header, Footer, Log
from textual.reactive import Reactive

"""
resources:
    https://textual.textualize.io/tutorial/
    https://textual.textualize.io/widgets/log/#__tabbed_1_2
"""

SHARC_ID = "409151d72b34"
MQTT_HOST = "wss.sharc.tech"
MQTT_PORT = 1883

# the code in these two functions is ugly but it's just to demontrate how it *could* work with Textualize
# without making huge modifications to what was here before
def print_sharc_event(console, note, sequence, message):
	console.write_line(f"[sharc:{SHARC_ID}] [sequence:{sequence}] {note} {message}")

def run_client(console):
    sharc = Client(MQTT_HOST, MQTT_PORT, SHARC_ID)
    sharc.on_available = lambda sequence, message: print_sharc_event(console, "Is Available:", sequence, message)
    sharc.on_version = lambda sequence, message: print_sharc_event(console, "Version:", sequence, message)
    sharc.on_reboot_count = lambda sequence, message: print_sharc_event(console, "Reboot Count:", sequence, message)
    sharc.on_network = lambda sequence, message: print_sharc_event(console, "Network:", sequence, message)
    sharc.on_sensor = lambda sequence, message: print_sharc_event(console, "Sensor:", sequence, message)
    sharc.on_mqtt = lambda sequence, message: print_sharc_event(console, "MQTT:", sequence, message)
    sharc.on_user = lambda sequence, message: print_sharc_event(console, "User:", sequence, message)
    sharc.on_io_s0 = lambda sequence, message: print_sharc_event(console, "S0:", sequence, message)
    sharc.on_io_s1 = lambda sequence, message: print_sharc_event(console, "S1:", sequence, message)
    sharc.on_io_s2 = lambda sequence, message: print_sharc_event(console, "S2:", sequence, message)
    sharc.on_io_s3 = lambda sequence, message: print_sharc_event(console, "S3:", sequence, message)
    sharc.on_ack = lambda sequence, message: print_sharc_event(console, "Ack:", sequence, message)
    sharc.connect()


class SharcInfo(Static):
    """emtpy for now"""

class Menu(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "reboot":
            # do something
            pass
        
        # elif button_id == "other":
            # ...

    def compose(self) -> ComposeResult:
        # basic header
        yield SharcInfo(f"Connected to {MQTT_HOST}:{MQTT_PORT} for device {SHARC_ID}")
        
        # add buttons to send MQTT commands or whatnot
        # you can make this look a lot better with some css (https://textual.textualize.io/guide/CSS/) but I suck at styling :P
        yield Button("Reboot", id="reboot")
        yield Button("Firmware Upgrade", id="firmware")
        yield Button("Some Other Action, I don't know", id="other")

class SharcClientUI(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Menu()
        yield Log()

    def on_ready(self) -> None:
        # create log and start MQTT client
        log = self.query_one(Log)
        log.write_line(">>> Start of console log")
        run_client(log)

if __name__ == "__main__":
    app = SharcClientUI()
    app.run()
