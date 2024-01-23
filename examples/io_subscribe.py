import paho.mqtt.client as mqtt
import json

SHARC_ID = '409151d72b34'
IO_REQUEST = {
  "id": "uuid123",
  "v": {
    "io.publish": True
  }
}

print(f'SHARC MQTT Namespace Docs: https://github.com/SharcTech/sharc-support#mqtt-namespace')


def on_connect(client, userdata, flags, rc):
    client.subscribe(f'sharc/{SHARC_ID}/evt/avail')
    client.subscribe(f'sharc/{SHARC_ID}/evt/sensor')


def on_message(client, userdata, msg):
    evt = msg.topic.split("/")[-1]
    payload = json.loads(msg.payload.decode("utf-8"))

    if evt == 'avail' and payload['v'] is False:
        print(f'SHARC {SHARC_ID} is OFFLINE')

    if evt == 'avail' and payload['v'] is True:
        print(f'SHARC {SHARC_ID} is ONLINE')

    if evt == 'sensor' and payload['v']['aggregate'] is False:
        print(f'SHARC {SHARC_ID} sensor aggregation is OFF')
        # each IO will come in on its own topic
        client.subscribe(f'sharc/{SHARC_ID}/evt/io/s0')
        client.subscribe(f'sharc/{SHARC_ID}/evt/io/s1')
        client.subscribe(f'sharc/{SHARC_ID}/evt/io/s2')
        client.subscribe(f'sharc/{SHARC_ID}/evt/io/s3')
        # ask SHARC for last IO reading... it might just be sitting there with no data changes
        client.publish(f'sharc/{SHARC_ID}/cmd/action', json.dumps(IO_REQUEST))

    if evt == 'sensor' and payload['v']['aggregate'] is True:
        print(f'SHARC {SHARC_ID} sensor aggregation is ON')
        # all IO will come in on the same topic
        client.subscribe(f'sharc/{SHARC_ID}/evt/io')
        # ask SHARC for last IO reading... it might just be sitting there with no data changes
        client.publish(f'sharc/{SHARC_ID}/cmd/action', json.dumps(IO_REQUEST))

    if evt == 'io':
        print(f'SHARC {SHARC_ID} IO {payload["v"]}')

    if evt in ['s0', 's1', 's2', 's3']:
        print(f'SHARC {SHARC_ID} IO/{evt} {payload["v"]}')


client = mqtt.Client(transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.connect("wss.sharc.tech", 1883, 60)
client.loop_forever()