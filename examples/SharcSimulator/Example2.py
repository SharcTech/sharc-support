from examples.SharcSimulator.Client import Client
import time


SHARC_ID = "deadbeef0000"
MQTT_HOST = "wss.sharc.tech"
MQTT_PORT = 1883


def print_sharc_command(command, message):
	print(f"[sharc:{SHARC_ID}] [command:{command}] {message}")


def on_connect(sharc):
	sharc.send_io_s0(0, "/")
	sharc.send_io_s1(0, "/")
	sharc.send_io_s2(0, "v")
	sharc.send_io_s3(4, "mA")


sharc = Client(MQTT_HOST, MQTT_PORT, SHARC_ID)
sharc.on_command = lambda command, message: print_sharc_command(command, message)
sharc.on_connect = on_connect
sharc.connect()
print("sharc connected")

sensor0_pnp_value = 0

while True:
	time.sleep(1)
	sensor0_pnp_value = 1 if sensor0_pnp_value == 0 else 0
	sharc.send_io_s0(sensor0_pnp_value, "/")

