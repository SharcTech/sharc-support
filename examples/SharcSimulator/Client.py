import paho.mqtt.client as mqtt
import json
import uuid


class Client:
	def __init__(self, host: str, port: int, sharc_id: str):
		self._host = host
		self._port = port
		self._keepalive = 60
		self._sharc_id = sharc_id
		self._is_connected = False
		self._mqttc = mqtt.Client(client_id=f"id_{str(uuid.uuid4())}")
		self._cb_cmd = None
		self._cb_on_connect = None
		self._msg_sequence = 0
		self._evt_base = f'sharc/{self._sharc_id}/evt/'

	def _make_evt_topic(self, event: str) -> str:
		return f'{self._evt_base}{event}'

	def _make_evt_message(self, value: bool | dict, sequence_override: int = None) -> dict:
		self._msg_sequence = self._msg_sequence + 1 if sequence_override is None else sequence_override
		return {
			"seq": self._msg_sequence,
			"v": value
		}

	def _make_evt_message_string(self, value, sequence_override=None) -> str:
		return json.dumps(self._make_evt_message(value, sequence_override))

	@property
	def is_connected(self):
		return self._is_connected

	@property
	def on_command(self):
		return self._cb_cmd

	@on_command.setter
	def on_command(self, f):
		self._cb_cmd = f

	@property
	def on_connect(self):
		return self._cb_cmd

	@on_connect.setter
	def on_connect(self, f):
		self._cb_on_connect = f

	def connect(self):
		self._mqttc.on_connect = self._on_connect
		self._mqttc.on_message = self._on_message
		self._mqttc.on_disconnect = self._on_disconnect
		self._mqttc.will_set(self._make_evt_topic("avail"), self._make_evt_message_string(False, -1), retain=True)
		self._mqttc.connect(host=self._host, port=self._port, keepalive=self._keepalive)
		self._mqttc.loop_start()

	def disconnect(self):
		self._send_unavailable()
		self._mqttc.disconnect()
		self._mqttc.loop_stop(force=False)

	def _on_connect(self, client, userdata, flags, rc):
		self._is_connected = True if rc == 0 else False
		self._mqttc.subscribe(f"sharc/{self._sharc_id}/cmd/#")
		self._send_available()
		self._send_version()
		self._send_reboot_counts()
		self._send_network()
		self._send_mqtt()
		if self._cb_on_connect is not None:
			self._cb_on_connect(self)

	def _on_message(self, client, userdata, message):
		segments = message.topic.split("/", 2)
		command = segments[2]
		payload = json.loads(message.payload.decode("utf-8"))
		if self._cb_cmd is not None:
			self._cb_cmd(command, payload)

	def _on_disconnect(self, client, userdata, rc):
		self._is_connected = False

	def _send_available(self):
		self._mqttc.publish(self._make_evt_topic("avail"), self._make_evt_message_string(True), retain=True)

	def _send_unavailable(self):
		self._mqttc.publish(self._make_evt_topic("avail"), self._make_evt_message_string(False), retain=True)

	def _send_version(self):
		value = {
			"serial": self._sharc_id,
			"sw": "DEV/FROZEN",
			"hw": "105",
			"fw": "ff00ff0",
			"model": "SHARC",
			"mfg": "Frenzy Engineering"
		}
		self._mqttc.publish(self._make_evt_topic("ver"), self._make_evt_message_string(value), retain=True)

	def _send_reboot_counts(self):
		value = {
			"watchdog_reset": 0,
			"power_on": 9,
			"deep_sleep": 0,
			"soft_reset": 0,
			"hard_reset": 11
		}
		self._mqttc.publish(self._make_evt_topic("rc"), self._make_evt_message_string(value), retain=True)

	def _send_network(self):
		value = {
			"dns": "192.168.88.1",
			"mask": "255.255.255.0",
			"mac": "deadbeef0000",
			"quality": 100,
			"ip": "192.168.88.254",
			"type": "LAN",
			"static": False,
			"gw": "192.168.88.1"
		}
		self._mqttc.publish(self._make_evt_topic("net"), self._make_evt_message_string(value), retain=True)

	def _send_sensor(self):
		value = {
			"aggregate": False,
			"calibrate": True,
			"convert": True,
			"s0": {
				"calibrate": "(v, False)",
				"convert": "(v, '/', False)",
				"period": 1000,
				"mode": "switch",
				"edge": "any",
				"persist": False
			},
			"s1": {
				"calibrate": "(v, False)",
				"convert": "(v, '/', False)",
				"period": 1000,
				"mode": "switch",
				"edge": "any",
				"persist": False
			},
			"s2": {
				"deadband": 100,
				"calibrate": "(v * 0.000384615, False)",
				"calibrated_range": [0, 0, 10],
				"convert": "(float('{:.1f}'.format((v - 0) / (10 - 0) * (10 - 0) + 0)), 'v', False)"
			},
			"s3": {
				"deadband": 100,
				"calibrate": "(v * 0.00075, False)",
				"calibrated_range": [0, 4, 20],
				"convert": "(float('{:.1f}'.format((v - 4) / (20 - 4) * (185 - 0) + 0)), 'psi', False)"
			}
		}
		self._mqttc.publish(self._make_evt_topic("sensor"), self._make_evt_message_string(value), retain=True)

	def _send_mqtt(self):
		value = {
			"user": "",
			"anonymous": True,
			"pass": "",
			"address": "wss.sharc.tech",
			"port": 1883
		}
		self._mqttc.publish(self._make_evt_topic("mqtt"), self._make_evt_message_string(value), retain=True)

	def _send_io_distinct(self, sensor_id, v, u):
		value = {
			sensor_id: {
				"v": v,
				"u": u
			}
		}
		self._mqttc.publish(self._make_evt_topic(f"io/{sensor_id}"), self._make_evt_message_string(value), retain=False)

	def send_io_s0(self, v, u):
		self._send_io_distinct("s0", v, u)

	def send_io_s1(self, v, u):
		self._send_io_distinct("s1", v, u)

	def send_io_s2(self, v, u):
		self._send_io_distinct("s2", v, u)

	def send_io_s3(self, v, u):
		self._send_io_distinct("s3", v, u)

	def send_user_data(self, value):
		self._mqttc.publish(self._make_evt_topic("user"), self._make_evt_message_string(value), retain=False)

