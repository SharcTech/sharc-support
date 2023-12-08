# SHARC Firmwares

## Update Instructions

### OTA

[SHARC Over-The-Air Updates Diagram](./sharc_ota_diagram.pdf)

#### App Update Instructions

1. Connect your SHARC to an MQTT broker.
2. Identify your SHARC's serial number (eg. `48e7290b118c`).
3. Connect to your SHARC using MQTT on the [Sharc Studio App](https://apps.apple.com/us/app/sharc-studio/id6447310295)
4. Go the Settings Tab
5. Click on the `Upload Firmware` Button Located Near the Bottom
6. Paste Your New Firmware .bin Link into the Text Box
7. Click `Upload`
8. Wait and Watch Your SHARC Device's LEDs to Ensure the Upgrade Finished Successfully [LED Status During Upgrade Process](https://github.com/SharcTech/sharc-support/blob/main/firmware/readme.md#led-status-during-upgrade-process)

#### Manual Update Instructions

1. Connect your SHARC to an MQTT broker.
2. Identify your SHARC's serial number (eg. `48e7290b118c`).
3. Set your MQTT publish topic to `sharc/{your-sharc-serial-number}/cmd/action` (eg. `sharc/48e7290b118c/cmd/action`).
4. Publish the following message with the appropriate firmware link.  Your SHARC must be able to access the URI without HTTP redirects.

```
{
  "id": "abc123",
  "v": {
    "device.ota": {
      "bin": "https://raw.githubusercontent.com/SharcTech/sharc-support/main/firmware/{new-firmware-filename.bin}"
    }
  }
}
```

5. Your SHARC will reboot and begin the update process.
6. After a successful update, your SHARC will boot into its first boot protocol and then reboot into production mode.  

#### LED Status During Upgrade Process

Observe your SHARC's LED to determine the success or failure of the OTA update.

| Stage | LED Color | Description | Success Result | Failure Result |
| ---   | ---       | --- | --- | --- |
| 1     | Magenta   | Initialize hardware and read the OTA instructions. | LED turns white. | LED turns red and reboots. |
| 2     | White     | Compose software services. | LED turns cyan. | LED turns red and reboots. |
| 3     | Cyan      | Establish network connection. | LED turns blue. | LED turns red and reboots. |
| 4     | Blue      | Retrieve firmware binary and write to filesystem. | LED turns green and reboots. | LED turns red and reboots. 

## Firmware List

| id | date-time | board version | is OTA | is RTM | comments |
| --- | --- | --- | --- | --- | --- | --- |
| [?](https://raw.githubusercontent.com/SharcTech/sharc-support/main/firmware/) | 12/08/2023 09:30 | 105 | yes | no | OTA Test |
| [ace8d12](https://raw.githubusercontent.com/SharcTech/sharc-support/main/firmware/ace8d12_ota.bin) | 12/08/2023 09:15 | 105 | yes | no | OTA Test |

