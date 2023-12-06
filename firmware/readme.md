# SHARC Firmwares

## Update Instructions

### OTA

#### Start the Update

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

eg.

```
{
  "id": "abc123",
  "v": {
    "device.ota": {
      "bin": "https://raw.githubusercontent.com/SharcTech/sharc-support/main/firmware/69b6f60_ota.bin"
    }
  }
}
```

5. Your SHARC will reboot and begin the update process.
6. After a successful update, your SHARC will boot into its first boot protocol and then reboot into production mode.

#### Update Process

Observe your SHARC's LED to determine the success or failure of the OTA update.

| Stage | LED Color | Description | Success Result | Failure Result |
| ---   | ---       | --- | --- | --- |
| 1     | Magenta   | Initialize hardware and read the OTA instructions. | LED turns white. | LED turns red and reboots. |
| 2     | White     | Compose software services. | LED turns cyan. | LED turns red and reboots. |
| 3     | Cyan      | Establish network connection. | LED turns blue. | LED turns red and reboots. |
| 4     | Blue      | Retrieve firmware binary and write to filesystem. | LED turns green and reboots. | LED turns red and reboots. 

## Firmware List

| id | date-time | board version | is OTA | is RTM | file | comments |
| --- | --- | --- | --- | --- | --- | --- |
| 8856501 | 12/06/2023 13:30 | 105 | yes | no | 8856501_ota.bin | OTA Test |
| 69b6f60 | 12/06/2023 12:10 | 105 | yes | no | 69b6f60_ota.bin | OTA Test |

