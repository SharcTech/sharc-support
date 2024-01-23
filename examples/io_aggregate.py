import paho.mqtt.client as mqtt
import json
import uuid

SHARC_ID = '409151d72b34'
COMMAND_TO_EXECUTE = "sensor_aggregation_on"

PENDING_COMMAND_ID = None
PENDING_REBOOT = False

COMMANDS = {
    "sensor_aggregation_on": {
        "type": "cfg",
        "v": {"sensor.aggregate": True}
    },
    "sensor_aggregation_off": {
        "type": "cfg",
        "v": {"sensor.aggregate": False}
    },
    "save_and_reboot": {
        "type": "action",
        "v": {"device.save.mqtt": True}
    }
}


print(f'SHARC MQTT Namespace Docs: https://github.com/SharcTech/sharc-support#mqtt-namespace')


def send_command(client, name):
    global PENDING_COMMAND_ID
    global COMMANDS
    if PENDING_COMMAND_ID is not None:
        print(f'Command is pending ID:{PENDING_COMMAND_ID}')
    else:
        PENDING_COMMAND_ID = str(uuid.uuid4())
        topic = f'sharc/{SHARC_ID}/cmd/{COMMANDS[name]["type"]}'
        payload = json.dumps({'id': PENDING_COMMAND_ID, 'v': COMMANDS[name]["v"]})
        print(f'Executing command TYPE: {name}, ID: {PENDING_COMMAND_ID}')
        print(f'... TOPIC: {topic}')
        print(f'... PAYLOAD: {payload}')
        client.publish(topic, payload)


def on_connect(client, userdata, flags, rc):
    client.subscribe(f'sharc/{SHARC_ID}/evt/avail')
    client.subscribe(f'sharc/{SHARC_ID}/evt/ack')


def on_message(client, userdata, msg):
    global PENDING_COMMAND_ID
    global PENDING_REBOOT
    evt = msg.topic.split("/")[-1]
    payload = json.loads(msg.payload.decode("utf-8"))

    if evt == 'avail' and payload['v'] is False:
        print(f'SHARC {SHARC_ID} is OFFLINE')

    if evt == 'avail' and payload['v'] is True:
        print(f'SHARC {SHARC_ID} is ONLINE')
        PENDING_REBOOT = True
        send_command(client, COMMAND_TO_EXECUTE)

    if evt == 'ack':
        if payload['v']['id'] == PENDING_COMMAND_ID:
            success = True if payload["v"]["rc"] == 0 else False
            print(f'Command acknowledged SUCCESS: {success}, ID: {PENDING_COMMAND_ID}')
            if success:
                PENDING_COMMAND_ID = None
                if PENDING_REBOOT is True:
                    PENDING_REBOOT = False
                    send_command(client, 'save_and_reboot')


client = mqtt.Client(transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.connect("wss.sharc.tech", 1883, 60)
client.loop_forever()