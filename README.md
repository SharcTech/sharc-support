# sharc-support
Sharc hardware, firmware, and software related support and discussions.

## Table of Contents

- [sharc-support](#sharc-support)
  - [Table of Contents](#table-of-contents)
  - [Links](#links)
  - [MQTT Namespace](#mqtt-namespace)
    - [MQTT EVENTS](#mqtt-events)
      - [MQTT Connect](#mqtt-connect)
      - [MQTT Disconnect](#mqtt-disconnect)
      - [Boot Counter](#boot-counter)
      - [Network Interface](#network-interface)
      - [Device Information](#device-information)
      - [MQTT Information](#mqtt-information)
      - [Sensor Values](#sensor-values)
        - [Mode: Aggregate](#mode-aggregate)
        - [Mode: Distinct](#mode-distinct)
        - [Mode: Aggregate-Calibrated-Converted](#mode-aggregate-calibrated-converted)
      - [Command Acknowledgement](#command-acknowledgement)
      - [User Data](#user-data)
    - [MQTT COMMANDS](#mqtt-commands)
      - [Actions](#actions)
        - [OTA](#ota)
        - [Device Network](#device-network)
        - [Device Reset](#device-reset)
        - [Configuration Save](#configuration-save)
        - [Reset Digital Input Counters](#reset-digital-input-counters)
        - [Publish IO Data](#publish-io-data)
        - [Set User Data](#set-user-data)
      - [Configuration Changes](#configuration-changes)
      - [Sensor Configuration](#sensor-configuration)
      - [All Sensors Report on Single Topic](#all-sensors-report-on-single-topic)
      - [Each Sensor Reports on Individual Topic](#each-sensor-reports-on-individual-topic)
      - [Digital Input - Switch](#digital-input---switch)
      - [Digital Input - Rising Edge Persisted Counter](#digital-input---rising-edge-persisted-counter)
      - [Digital Input - Falling Edge Accumulator](#digital-input---falling-edge-accumulator)
      - [Analog Input - Custom Conversion](#analog-input---custom-conversion)
        - [Network Example](#network-example)
        - [Broker Example](#broker-example)
      - [List of Avaialble Settings](#list-of-avaialble-settings)
  - [Self-hosting Sharc Studio](#self-hosting-sharc-studio)
    - [If Not Using `localhost` To Connect To Sharc UI, You Must Allow Bluetooth From Insecure Connection](#if-not-using-localhost-to-connect-to-sharc-ui-you-must-allow-bluetooth-from-insecure-connection)
      - [To enable this setting](#to-enable-this-setting)
    - [To Run Locally (MQTT Broker already setup | Without compose)](#to-run-locally-mqtt-broker-already-setup--without-compose)
    - [To Run Locally (MQTT Broker already setup | With compose)](#to-run-locally-mqtt-broker-already-setup--with-compose)
    - [To Run Locally (MQTT Broker not setup | With docker-compose)](#to-run-locally-mqtt-broker-not-setup--with-docker-compose)

## Links

[Data Sheet](https://www.mriiot.com/s/SHARC-Data-Sheet-Latest.pdf)  

[Setup Instructions](https://www.mriiot.com/s/SHARC-Setup-Instructions.pdf)  

[Cloud Sharc Studio](https://sharc.tech/)

[iOS Sharc Studio](https://apps.apple.com/us/app/sharc-studio/id6447310295)

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
    "power_on": 0,
    "hard_reset": 0,
    "watchdog_reset": 0,
    "deep_sleep": 0,
    "soft_reset": 0
  }
}
```

`$.v.power_on` - [int] Power_On count.  
`$.v.hard_reset` - [int] Hard count.  
`$.v.watchdog_reset` - [int] WDT count.  
`$.v.deep_sleep` - [int] Deep_Sleep count.  
`$.v.soft_reset` - [int] Soft count.  

#### Network Interface

Current network interface values, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/net`  
Retain: `true`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "type": "WLAN",
    "static": false,
    "ip": "0.0.0.0",
    "gw": "0.0.0.0",
    "mask": "0.0.0.0",
    "dns": "0.0.0.0",
    "mac": "deadbeef",
    "quality": 100,
    "ssid": "wifi-name",
    "lan_fallback_s": 120
  }
}
```

`$.v.type` - [string] Current network type of WLAN or LAN.  
`$.v.static` - [bool] Whether the IP configuration is static or dynamic.  
`$.v.ip` - [string] Device IP Address.  
`$.v.gw` - [string] Gateway IP Address.  
`$.v.mask` - [string] Subnet mask.  
`$.v.dns` - [string] DNS Server IP Address.  
`$.v.mac` - [string] Device Hardware Address.  
`$.v.quality` - [int] Connection quality.  
`$.v.ssid` - [string] (WLAN only)  Wifi network name.    
`$.v.lan_fallback` - [int] (WLAN only)  Seconds to wait for Wifi connection before rebooting into LAN.  Zero to disable this feature.  

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
    "sw": "RTM/FROZEN"
  }
}
```

`$.v.mfg` - [string] Hardware manufacturer.  
`$.v.model` - [string] Hardware model.  
`$.v.serial` - [string] Hardware serial number.  
`$.v.hw` - [string] Hardware version.  
`$.v.fw` - [string] Firmware version.  
`$.v.sw` - [string] Software version.  

#### MQTT Information

MQTT connection information, published upon connection.  

Topic: `sharc/{{sharc_id}}/evt/mqtt`  
Retain: `true`  
Payload:  

```json
{
  "seq": 1,
  "v": {
    "address": "192.168.5.5",
    "port": 1883,
    "user": "",
    "anonymous": true
  }
}
```

`$.v.address` - [string] Broker address.  
`$.v.port` - [int] Broker port.  
`$.v.user` - [string] Username.  
`$.v.anonymous` - [bool] Is connection anonymous.  

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

##### OTA

Initiates over-the-air updates over WIFI or Ethernet.  
  
Once the device receives this message, it will:

* Reboot into update mode.
* Download the new firmware binary.
* Install the new firmware binary.
* Reboot into first-run mode.
* Reboot into production mode.

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": {
    "device.ota": {
      "bin": "direct-download-uri-to-binary"
    }
  }
}
```

##### Device Network

Select between WLAN and LAN network.  Device reset is required to take effect.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "device.network.wlan" : true
  }
}
```

```json
{
  "id": "abc123",
  "v": { 
    "device.network.lan" : true
  }
}
```

##### Device Reset

Discard configuration changes and reset device into MQTT.  

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

```json
{
  "id": "abc123",
  "v": { 
    "device.reset.mqtt" : true
  }
}
```

Discard configuration changes and reset device into BLE.  

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "device.reset.ble" : true
  }
}
```

##### Configuration Save

Save configuration and reset device into MQTT.   

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "device.save" : true
  }
}
```

```json
{
  "id": "abc123",
  "v": { 
    "device.save.mqtt" : true
  }
}
```

Save configuration and reset device into BLE.    

Topic: `sharc/{{sharc_id}}/cmd/action`  
Retain: `false`  
Payload:  

```json
{
  "id": "abc123",
  "v": { 
    "device.save.ble" : true
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

#### List of Avaialble Settings


| Section | Item                     | Legend | Description                                                | Access | Value Type | Default                                 | Notes                                                                                                 |   |
|---------|--------------------------|--------|------------------------------------------------------------|--------|------------|-----------------------------------------|-------------------------------------------------------------------------------------------------------|---|
| lan     |                          |        | Ethernet Configuration.                                    |        | object     |                                         |                                                                                                       |   |
|         | lan.static_ip            |        | Static configuration or DHCP.                              | RW     | boolean    | false                                   |                                                                                                       |   |
|         | lan.wait_for_ip          |        | Wait for IP address before completing boot process.        | RW     | boolean    | false                                   |                                                                                                       |   |
|         | lan.timeout_ms           |        | Milliseconds to wait for network, if wait_for_ip is false. | RW     | integer    | 1000                                    | milliseconds                                                                                          |   |
|         | lan.ip_config.ip         |        | Statically assigned device IP address.                     | RW     | string     | 192.168.5.5                             | four octet                                                                                            |   |
|         | lan.ip_config.mask       |        | Statically assigned network mask.                          | RW     | string     | 255.255.255.0                           | four octet                                                                                            |   |
|         | lan.ip_config.gw         |        | Statically assigned gateway IP address.                    | RW     | string     | 192.168.5.1                             | four octet                                                                                            |   |
|         | lan.ip_config.dns        |        | Statically assigned DNS server IP address.                 | RW     | string     | 8.8.8.8                                 | four octet                                                                                            |   |
| wlan    |                          |        | n/a                                                        |        | object     |                                         |                                                                                                       |   |
|         | wlan.static_ip           |        | Static configuration or DHCP.                              | RW     | boolean    | false                                   |                                                                                                       |   |
|         | wlan.ssid                |        | Wifi network name.                                         | RW     | string     | (empty)                                 |                                                                                                       |   |
|         | wlan.pass                |        | Wifi network password.                                     | W      | string     | (empty)                                 |                                                                                                       |   |
|         | wlan.ip_config.ip        |        | Statically assigned device IP address.                     | RW     | string     | 192.168.5.5                             | four octet                                                                                            |   |
|         | wlan.ip_config.mask      |        | Statically assigned network mask.                          | RW     | string     | 255.255.255.0                           | four octet                                                                                            |   |
|         | wlan.ip_config.gw        |        | Statically assigned gateway IP address.                    | RW     | string     | 192.168.5.1                             | four octet                                                                                            |   |
|         | wlan.ip_config.dns       |        | Statically assigned DNS server IP address.                 | RW     | string     | 8.8.8.8                                 | four octet                                                                                            |   |
| mqtt    |                          |        | MQTT configuration.                                        |        | object     |                                         |                                                                                                       |   |
|         | mqtt.seq_reset           |        | Reset sequence number when reconnecting.                   | RW     | boolean    | false                                   |                                                                                                       |   |
|         | mqtt.broker.address      |        | Broker IP address.                                         | RW     | string     | 192.168.5.4                             | four octet                                                                                            |   |
|         | mqtt.broker.port         |        | Broker port.                                               | RW     | integer    | 1883                                    |                                                                                                       |   |
|         | mqtt.broker.user         |        | Broker username. Keep blank for anonymous.                 | RW     | string     | (empty)                                 |                                                                                                       |   |
|         | mqtt.broker.pass         |        | Broker password. Keep blank for anonymous.                 | W      | string     | (empty)                                 |                                                                                                       |   |
|         | mqtt.broker.ka_s         |        | Keepalive seconds.                                         | RW     | integer    | 60                                      | seconds                                                                                               |   |
|         | mqtt.broker.ping_s       |        | Seconds between pings.                                     | RW     | integer    | 5                                       | seconds                                                                                               |   |
| sensor  |                          |        | Sensor output configuration.                               |        | object     |                                         |                                                                                                       |   |
|         | sensor.aggregate         |        | Publish sensor values as a single payload.                 | RW     | boolean    | true                                    |                                                                                                       |   |
|         | sensor.calibrate         |        | Calibrate sensor values.                                   | RW     | boolean    | true                                    |                                                                                                       |   |
|         | sensor.convert           |        | Convert sensor values.                                     | RW     | boolean    | true                                    |                                                                                                       |   |
| sensor.s0 |                        |        | Binary PNP Sensor.                                         |        | object     |                                         |                                                                                                       |   |
|         | sensor.s0.calibrate      |        | Calibration formula.                                       | RW     | string     | (v, False)                              |                                                                                                       |   |
|         | sensor.s0.convert        |        | Conversion formula.                                        | RW     | string     | (v, '/', False)                         | see [RFC8428](https://datatracker.ietf.org/doc/rfc8428/)                                              |   |
|         | sensor.s0.mode           |        | `switch`, `counter`, or `accumulator`.                     | RW     | string     | switch                                  |                                                                                                       |   |
|         | sensor.s0.edge           |        | `any`, `rising`, `falling`.                                | RW     | string     | any                                     |                                                                                                       |   |
|         | sensor.s0.period         |        | Accumulator report period.                                 | RW     | integer    | 1000                                    | milliseconds                                                                                          |   |
| sensor.s1 |                        |        | Binary NPN Sensor.                                         |        | object     |                                         |                                                                                                       |   |
|         | sensor.s1.calibrate      |        | Calibration formula.                                       | RW     | string     | (v, False)                              |                                                                                                       |   |
|         | sensor.s1.convert        |        | Conversion formula.                                        | RW     | string     | (v, '/', False)                         | see [RFC8428](https://datatracker.ietf.org/doc/rfc8428/)                                              |   |
|         | sensor.s1.mode           |        | `switch`, `counter`, or `accumulator`.                     | RW     | string     | switch                                  |                                                                                                       |   |
|         | sensor.s1.edge           |        | `any`, `rising`, `falling`.                                | RW     | string     | any                                     |                                                                                                       |   |
|         | sensor.s1.period         |        | Accumulator report period.                                 | RW     | integer    | 1000                                    | milliseconds                                                                                          |   |
| sensor.s2 |                        |        | Analog Voltage Sensor.                                     |        | object     |                                         |                                                                                                       |   |
|         | sensor.s2.deadband       |        | Sensor dead-zone.                                          | RW     | integer    | 100                                     | a value of 30 is 0.01V                                                                                   |   |
|         | sensor.s2.calibrate      |        | Calibration formula.                                       | RW     | string     | (v * 0.000384615, False)                |                                                                                                       |   |
|         | sensor.s2.convert        |        | Conversion formula.                                        | RW     | string     | (float('{:.1f}'.format((v - 0) / (10 - 0) * (10 - 0) + 0)), 'v', False)         | see [RFC8428](https://datatracker.ietf.org/doc/rfc8428/)                                              |   |
| sensor.s3 |                        |        | Analog Current Sensor.                                     |        | object     |                                         |                                                                                                       |   |
|         | sensor.s3.deadband       |        | Sensor dead-zone.                                          | RW     | integer    | 100                                     | a value of 10 is 0.01mA                                                                                 |   |
|         | sensor.s3.calibrate      |        | Calibration formula.                                       | RW     | string     | (v * 0.00075, False)                    |                                                                                                       |   |
|         | sensor.s3.convert        |        | Conversion formula.                                        | RW     | string     | (float('{:.1f}'.format((v - 4) / (20 - 4) * (20 - 4) + 4)), 'mA', False)         | see [RFC8428](https://datatracker.ietf.org/doc/rfc8428/)                                              |   |


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

### To Run Locally (MQTT Broker already setup | With compose)
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
