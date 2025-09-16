# WaterBed
Water cooled bed controlled by Seeed Studio esp32c3 through MQTT as an IoT device.

### Accomplishments
- Use of ESP-IDF to build, flash, and monitor device through CLI instead of using ArduinoIDE and PlatformIO.
- Use of Arduino component library instead of ESP-IDF for simpler code.
- First ever practical circuit:
    - Move to perf|proto board instead of staying on breadboard.
    - Learned use of MOSFETs, Optocouplers.
    - Use of surface-mount device (SMD), and so ability to buy and store larger quantity of components in smaller format.


### Failures
- Serial.prints don't work due to using GPIO 20 and so having to disable UART.
- Was unable to "sniff" data going to AiP650e chip that was driving 7-segment displays, and so was unable to capture useful data such as current temp, target, temp units.


### Things learned
- Sticking with Arduino component library (2.24GB) is heavy on build times and size (This plus MQTT required a larger partition size). Consider moving to ESP-IDF vanilla.
- Be more careful when choosing GPIO pins, as some should not be used (e.g. GPIO 10 used to change boot up).
- Some PCBs have a clear film. Need to remove that before trying to solder.