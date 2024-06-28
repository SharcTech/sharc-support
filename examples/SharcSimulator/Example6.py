from examples.SharcSimulator.Client import Client
import time
import random


SHARC_ID = "deadbeef0000"
MQTT_HOST = "192.168.111.46"
MQTT_PORT = 1883


def print_sharc_command(command, message):
	print(f"[sharc:{SHARC_ID}] [command:{command}] {message}")


def on_connect(sharc):
	sharc.send_io_s0(0, "count")
	sharc.send_io_s1(0, "/")
	sharc.send_io_s2(0, "v")
	sharc.send_io_s3(0, "mA")


sharc = Client(MQTT_HOST, MQTT_PORT, SHARC_ID)
sharc.on_command = lambda command, message: print_sharc_command(command, message)
sharc.on_connect = on_connect
sharc.connect()
print("sharc connected")

sensor0_pnp_value = 0
cycle_start = time.monotonic()

while True:
	time.sleep(random.uniform(2.0, 6.0))
	sensor0_pnp_value += 1
	sharc.send_io_s0(sensor0_pnp_value, "count")
	sharc.send_user_data({
		"cycle_time_s": round(time.monotonic() - cycle_start, 2)
	})
	cycle_start = time.monotonic()


