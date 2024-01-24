from examples.SharcClient.Client import Client
import time


SHARC_ID = "409151d72b34"
MQTT_HOST = "wss.sharc.tech"
MQTT_PORT = 1883


def print_sharc_event(note, sequence, message):
	print(f"[sharc:{SHARC_ID}] [sequence:{sequence}] {note} {message}")


sharc = Client(MQTT_HOST, MQTT_PORT, SHARC_ID)
sharc.on_available = lambda sequence, message: print_sharc_event("Is Available:", sequence, message)
sharc.on_version = lambda sequence, message: print_sharc_event("Version:", sequence, message)
sharc.on_reboot_count = lambda sequence, message: print_sharc_event("Reboot Count:", sequence, message)
sharc.on_network = lambda sequence, message: print_sharc_event("Network:", sequence, message)
sharc.on_sensor = lambda sequence, message: print_sharc_event("Sensor:", sequence, message)
sharc.on_mqtt = lambda sequence, message: print_sharc_event("MQTT:", sequence, message)
sharc.on_user = lambda sequence, message: print_sharc_event("User:", sequence, message)
sharc.on_io_s0 = lambda sequence, message: print_sharc_event("S0:", sequence, message)
sharc.on_io_s1 = lambda sequence, message: print_sharc_event("S1:", sequence, message)
sharc.on_io_s2 = lambda sequence, message: print_sharc_event("S2:", sequence, message)
sharc.on_io_s3 = lambda sequence, message: print_sharc_event("S3:", sequence, message)
sharc.on_ack = lambda sequence, message: print_sharc_event("Ack:", sequence, message)
sharc.connect()

while True:
	choice = input()
	choice = choice.lower()

	if choice == 'io':
		sharc.request_io()
