# sharc-support
Sharc hardware, firmware, and software related support and discussions.

## Table of Contents
[MQTT Payloads](#mqtt-namespace)
  [MQTT Events](#mqtt-events)
  [MQTT Commands](#mqtt-commands)
[Self-hosting Sharc Studio](#self-hosting-sharc-studio)

## Links

[Data Sheet](https://www.mriiot.com/s/SHARC-Data-Sheet-Latest.pdf)  

[Setup Instructions](https://www.mriiot.com/s/SHARC-Setup-Instructions.pdf)  

[Cloud Sharc Studio](https://sharc.tech/)

[iOS Sharc Studio]() -- TODO: link

## MQTT Namespace

### MQTT EVENTS

Topic structure: `sharc/{{sharc_id}}/evt/{{name}}`  

#### MQTT Connect

Availability, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/avail`  
Retain: `true`  
Payload: 
```json
{
  "seq": 0,
  "v": true
}
```

#### MQTT Disconnect

Device disconnect message is published by MQTT broker LWT mechanism.  

Topic: `sharc/{{sharc_id}}/evt/avail`  
Retain: `true`  
Payload:  

```json
{
  "seq": -1,
  "v": false
}
```

#### Boot Counter

Reboot causes and counters, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/rc`  
Retain: `true`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0
  }
}
```

`$.v.0` - [int] Power_On count.  
`$.v.1` - [int] Hard count.  
`$.v.2` - [int] WDT count.  
`$.v.3` - [int] Deep_Sleep count.  
`$.v.4` - [int] Soft count.  

#### Network Interface

Current network interface values, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/net`  
Retain: `true`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "static": false,
    "ip": "0.0.0.0",
    "gw": "0.0.0.0",
    "mask": "0.0.0.0",
    "dns": "0.0.0.0",
    "mac": "deadbeef"
  }
}
```

`$.v.static` - [boolean] Whether the IP configuration is static or dynamic.  
`$.v.ip` - [string] Device IP Address.  
`$.v.gw` - [string] Gateway IP Address.  
`$.v.mask` - [string] Subnet mask.  
`$.v.dns` - [string] DNS Server IP Address.  
`$.v.mac` - [string] Device Hardware Address.  

#### Device Information

Device information, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/ver`  
Retain: `true`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "mfg": "MRIIOT",
    "model": "SHARC",
    "serial": "{chip-id}",
    "hw": "105",
    "fw": "{git-head}",
    "sw": "{git-head}"
  }
}
```

`$.v.mfg` - [string] Hardware manufacturer.  
`$.v.model` - [string] Hardware model.  
`$.v.serial` - [string] Hardware serial number.  
`$.v.hw` - [string] Hardware version.  
`$.v.fw` - [string] Firmware version.  
`$.v.sw` - [string] Software version.  

#### Sensor Values

Values read from sensors.  

Settings and their effects:  
  
* `sensor.aggregate`:  
    * `true`: all sensors published on a single topic, packed into a single JSON object.  
    * `false`: each sensor published on its own topic.  
* `sensor.calibrate`:  
    * `true`: each sensor's `calibrate` property is evaluated before publishing.  
    * `false`: evaluation of `calibrate` property is omitted.  
* `sensor.convert`:  
    * `true`: each sensor's `convert` property is evaluated before publishing.  
    * `false`: evaluation of `convert` property is omitted.  

##### Mode: Aggregate

Setting: `sensor.aggregate = true` and `sensor.calibrate = false|true` and `sensor.convert = false`.  
Description: All sensors published on a single topic, uncalibrated and unconverted values.  
Topic: `sharc/{{sharc_id}}/evt/io`  
Retain: `false`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "s0": 0,
    "s1": 0,
    "s2": 0,
    "s3": 0
  }
}
```

`$.v.s0` - [int] PNP sensor state.  
&nbsp;&nbsp;&nbsp;`0` - off  
&nbsp;&nbsp;&nbsp;`1` - on  
`$.v.s1` - [int] NPN sensor state.  
&nbsp;&nbsp;&nbsp;`0` - off  
&nbsp;&nbsp;&nbsp;`1` - on  
`$.v.s2` - [decimal] Voltage sensor value.  
&nbsp;&nbsp;&nbsp;`0` - minimum bits  
&nbsp;&nbsp;&nbsp;`32767` - maximum bits  
`$.v.s3` - [decimal] Ampere sensor value.  
&nbsp;&nbsp;&nbsp;`0` - minimum bits  
&nbsp;&nbsp;&nbsp;`32767` - maximum bits  

##### Mode: Distinct

Setting: `sensor.aggregate = false` and `sensor.calibrate = false` and `sensor.convert = false`.  
Description: Each sensor published on its own topic, uncalibrated and unconverted values.  
Topic: `sharc/{{sharc_id}}/evt/io/{{sensor_name}}`  
Retain: `false`  
Payload:  

```json
{
  "seq": 1,
  "v": 0
}
```

##### Mode: Aggregate-Calibrated-Converted

Setting: `sensor.aggregate = true` and `sensor.calibrate = true` and `sensor.convert = true`.  
Description: All sensors published to a single topic, calibrated and converted values. Units defined in [RFC8428](https://datatracker.ietf.org/doc/rfc8428/).  
Topic: `sharc/{{sharc_id}}/evt/io`  
Retain: `false`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "s0": {
      "v": 0.0,
      "u": "/"
    },
    "s1": {
      "v": 1.0,
      "u": "/"
    },
    "s2": {
      "v": 10,
      "u": "V"
    },
    "s3": {
      "v": 100,
      "u": "Cel"
    }
  }
}
```

`$.v.s0` - [any] PNP sensor.  

&nbsp;&nbsp;&nbsp;`v` - value  
&nbsp;&nbsp;&nbsp;`u` - units  
`$.v.s1` - [any] NPN sensor state.  

&nbsp;&nbsp;&nbsp;`v` - value  
&nbsp;&nbsp;&nbsp;`u` - units  
`$.v.s2` - [any] Voltage sensor value.  

&nbsp;&nbsp;&nbsp;`v` - value  
&nbsp;&nbsp;&nbsp;`u` - units  
`$.v.s3` - [any] Ampere sensor value.  

&nbsp;&nbsp;&nbsp;`v` - value  
&nbsp;&nbsp;&nbsp;`u` - units  

#### Command Acknowledgement

Acknowledgement of command execution.  

Topic: `sharc/{{sharc_id}}/evt/ack`  
Retain: `false`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "id": "abc123",
    "rc": 0
  }
}
```

`$.v.id` - [string] Correlation to command.  
`$.v.rc` - [int] Command execution result code.  
&nbsp;&nbsp;&nbsp;`0` - success  
&nbsp;&nbsp;&nbsp;`non-zero` - failure code

#### User Data

Data published from user script.  


Topic: `sharc/{{sharc_id}}/evt/user`  
Retain: `false`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "user": "object"
  }
}
```

`$.v` - [any] User data.  

### MQTT COMMANDS

Topic structure: `sharc/{{sharc_id}}/cmd/{{name}}`  

Each command payload must include a unique `id` attribute.  
This value is published back as an acknowledgement of command execution status.  
Commands with the `id` attribute are dropped.  

#### Actions

##### Device Reset

Discard configuration changes and reset device.  

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "device.reset" : true
  }
}
```

##### Configuration Save

Save configuration and reset device.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "cfg.save" : true
  }
}
```

##### Reset Digital Input Counters

Reset digital input counters.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "di.counter.reset" : true
  }
}
```

##### Publish IO Data

Request IO data publish.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "io.publish" : true
  }
}
```

##### Set User Data

Set user data in user script.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "ud.set" : {
      "user": "object"
    }
  }
}
```

#### Configuration Changes

Changes value in configuration.  
`cfg.save` action required to persist changes to flash.  
  
Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": {
    "config.key1": "value",
    "config.key2": "value"
  }
}
```

`$.v.<path>` - [bool|number|string|null] Configuration value.  `path` can be any valid path within the configuration file.

#### Sensor Configuration

Changes sensor modes via the configuration topic.  
`cfg.save` action required to persist changes to flash.  

#### All Sensors Report on Single Topic

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.aggregate": true
  }
}
```

#### Each Sensor Reports on Individual Topic

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.aggregate": false
  }
}
```

#### Digital Input - Switch

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.s0.mode": "switch",
    "sensor.s0.calibrate": "(v, False)",
    "sensor.s0.convert": "(v, '/', False)"
  }
}
```

#### Digital Input - Rising Edge Persisted Counter

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.s0.mode": "counter",
    "sensor.s0.edge": "rising",
    "sensor.s0.persist": true,
    "sensor.s0.calibrate": "(v, False)",
    "sensor.s0.convert": "(v, 'count', False)"
  }
}
```

#### Digital Input - Falling Edge Accumulator

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.s0.mode": "accumulator",
    "sensor.s0.edge": "falling",
    "sensor.s0.period": 1000,
    "sensor.s0.calibrate": "(v, False)",
    "sensor.s0.convert": "(v, 'count', False)"
  }
}
```

#### Analog Input - Custom Conversion

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`  
Payload:  
  
```json
{
  "id": "abc123",
  "v": {
    "sensor.s3.convert": "(({v} - 4) * (100 - 0) / (20 - 4) + 0, 'Cel', False)"
  }
}
```

##### Network Example

Network configuration. Reset required.  

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`

<details><summary>Payload - Enforcing static IP assignment.</summary>
<p>

```json
{
  "id": "abc123",
  "v": {
    "lan.static_ip": 1,
    "lan.ip_config.ip": "192.168.1.55",
    "lan.ip_config.gw": "192.168.1.1",
    "lan.ip_config.mask": "255.255.255.0",
    "lan.ip_config.dns": "8.8.8.8"
  }
}
```

</p>
</details>

<details><summary>Payload - Enforcing DHCP.</summary>
<p>

```json
{
  "id": "abc123",
  "v": {
    "lan.static_ip": 0
  }
}
```

</p>
</details>

<details><summary>Payload - Wait for IP address on boot before continuing.</summary>
<p>

```json
{
  "id": "abc123",
  "v": {
    "lan.wait_for_ip": 1
  }
}
```

</p>
</details>

<details><summary>Payload - Do not wait for IP address on boot before continuing.  Instead, wait for a specific duration in milliseconds.</summary>
<p>

```json
{
  "id": "abc123",
  "v": {
    "lan.wait_for_ip": 0,
    "lan.timeout": 1000
  }
}
```

</p>
</details>

##### Broker Example

Broker configuration. Reset required.  

Topic: `sharc/{{sharc_id}}/cmd/cfg`  
Retain: `false`

<details><summary>Payload - Set broker options.</summary>
<p>

```json
{
  "id": "abc123",
  "v": {
    "mqtt.broker.address": "broker.xyz",
    "mqtt.broker.port": 1883,
    "mqtt.broker.user": "",
    "mqtt.broker.pass": "",
    "mqtt.broker.ka": 60,
    "mqtt.broker.ping": 5
  }
}
```

</p>
</details>


## Self-hosting Sharc Studio

### If Not Using `localhost` To Connect To Sharc UI, You Must Allow Bluetooth From Insecure Connection
#### To enable this setting
1. Navigate to [chrome://flags](chrome://flags)
2. Search for `Insecure origins treated as secure` flag 
3. Enable option and provide domain/IP you are trying to connect to
4. Relaunch
5. Navigate to `http://your_server_address`
6. You will now be able to use bluetooth from the browser

### To Run Locally (MQTT Broker already setup | Without compose)
1. Ensure you have Docker installed  
    a. If you do not, follow [https://docs.docker.com/](https://docs.docker.com/) installation instructions for your OS
2. Open a terminal window
3. Pull the `Sharc-Tech` image using `docker pull ladder99/sharc-ui:latest`
4. Run the image inside of a container using `docker run -d -p 80:80 ladder99/sharc-ui:latest`
5. Navigate to [https://localhost/](https://localhost/) in your browser
6. If you already have a MQTT Broker set up you are good to go!

### To Run Locally (MQTT Broker already setup | Without compose)
1. Ensure you have Docker and Docker Compose installed
    1. If you do not, follow [https://docs.docker.com/](https://docs.docker.com/) installation instructions for your OS
2. Create a file named `docker-compose.yml`
3. Copy this configuration into the file:
```
version: "3.9"

services:

  sharc-ui:
    image: ladder99/sharc-ui:latest
    container_name: sharc_tech
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "1m"
    ports:
      - "80:80/tcp"
```
4. Go to directory that the file is located in 
5. Run `docker compose up -d` in the terminal
6. Navigate to [https://localhost/](https://localhost/) in your browser
7. If you already have a MQTT Broker set up you are good to go!



### To Run Locally (MQTT Broker not setup | With docker-compose)
1. Ensure you have Docker and Docker Compose installed
    1. If you do not, follow [https://docs.docker.com/](https://docs.docker.com/) installation instructions for your OS
2. Create a file named `docker-compose.yml`
    1. Make sure to note down where this file is created.
3. Copy this configuration into the file:
```
version: "3.9"

services:

  sharc-ui:
    image: ladder99/sharc-ui
    container_name: sharc_tech
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "1m"
    environment:
      - REACT_APP_BROKER_IP=wss.sharc.tech
      - REACT_APP_BROKER_PORT=443
    ports:
      - "80:80/tcp"

  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883/tcp"
      - "9001:9001/tcp"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
      - /home/your_username/volumes/mosquitto/config:/mosquitto/config:rw
      - /home/your_username/volumes/mosquitto/data:/mosquitto/data:rw
      - /home/your_username/volumes/mosquitto/log:/mosquitto/log:rw
    logging:
      driver: "json-file"
      options:
        max-size: "20m"
```
6. Ensure that you replace `your_username` with the username of your computer
3. Go to the directory of the file created in step 2
4. Run `docker compose up -d` in the terminal
7. Go to the newly created volume directory at `/home/your_username/volumes/mosquitto/config`
8. Create a file named `mosquitto.conf`
9. Copy this text into the file and save:
```
connection_messages true
log_dest stdout
log_dest stderr
log_timestamp true
log_type all
max_inflight_bytes 1000000
max_inflight_messages 1
max_queued_bytes 2000000
max_queued_messages 1000
message_size_limit 1500
persistence false
queue_qos0_messages false
retain_available true
per_listener_settings true
listener 1883 0.0.0.0
protocol mqtt
allow_anonymous true
max_connections 100
socket_domain ipv4
allow_zero_length_clientid false
listener 9001 0.0.0.0
protocol websockets
allow_anonymous true
max_connections 100
socket_domain ipv4
allow_zero_length_clientid false
```

This will ensure that your broker is set up to allow websocket connections on port 9001

6. Navigate to [https://localhost/](https://localhost/) in your browser
7. Congrats! You now have both Sharc-Tech and a MQTT Broker running locally