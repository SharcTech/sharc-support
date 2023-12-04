# SHARC Firmwares

## Update Instructions

### OTA

#### Start the Update

1. Connect your SHARC to an MQTT broker.
2. Identify your SHARC's serial number (eg. 48e7290b118c).
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

eg.

```
{
  "id": "abc123",
  "v": {
    "device.ota": {
      "bin": "https://raw.githubusercontent.com/SharcTech/sharc-support/main/firmware/507764c_ota.bin"
    }
  }
}
```

5. Your SHARC will reboot and begin the update process.

#### Update Process

Observe your SHARC's LED to determine the success or failure of the OTA update.

| Stage | LED Color | Description | Success Result | Failure Result |
| ---   | ---       | --- | --- | --- |
| 1     | Magenta   | Initialize hardware and read the OTA instructions. | LED turns white. | LED turns red and reboots. |
| 2     | White     | Compose software services. | LED turns cyan. | LED turns red and reboots. |
| 3     | Cyan      | Establish network connection. | LED turns blue. | LED turns red and reboots. |
| 4     | Blue      | Retrieve firmware binary and write to filesystem. | LED turns green and reboots. | LED turns red and reboots. 

## Firmware List

| id | date-time | board version | is OTA | file | comments |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 507764c | 12/04/2023 11:00 | 105 | yes | 507764c_ota.bin | initial firmware release supporting OTA |

