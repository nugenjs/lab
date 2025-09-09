# ESP32-C3 Arduino-style Blink Project

This project demonstrates how to use ESP-IDF with Arduino-style functions to create a simple LED blink program for the Seeed ESP32-C3 board. Instead of using the full Arduino framework, we implement Arduino-style functions using native ESP-IDF calls for better performance and smaller footprint.

## Hardware Requirements

- Seeed ESP32-C3 development board
- USB-C cable for programming and power

## Features

- Uses native ESP-IDF with Arduino-style function wrappers
- Blinks the onboard LED (GPIO2) every 1 second
- ESP_LOG output to monitor LED state
- Optimized configuration for ESP32-C3
- Smaller memory footprint compared to full Arduino framework

## Pin Configuration

- **LED Pin**: GPIO2 (onboard LED on Seeed ESP32-C3)

## Arduino-style Functions Implemented

- `pinMode(pin, mode)` - Set GPIO pin mode
- `digitalWrite(pin, value)` - Set GPIO pin level
- `delay(ms)` - Delay in milliseconds

## Prerequisites

1. **ESP-IDF**: Install ESP-IDF v5.0 or later
   ```bash
   # Follow the official ESP-IDF installation guide
   # https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/get-started/
   ```

## Building and Flashing

1. **Set up the environment**:
   ```bash
   # Source the ESP-IDF environment
   . $HOME/esp/esp-idf/export.sh
   ```

2. **Configure the project**:
   ```bash
   cd /Users/jngu3012/dev/lab/microcontrol/esp32/03espIdfArduinoLib
   idf.py set-target esp32c3
   idf.py menuconfig  # Optional: modify configuration if needed
   ```

3. **Build the project**:
   ```bash
   idf.py build
   ```

4. **Flash to the board**:
   ```bash
   # Connect your Seeed ESP32-C3 via USB-C
   idf.py -p /dev/cu.usbmodem* flash monitor
   ```
   
   Replace `/dev/cu.usbmodem*` with the actual port name. On macOS, you can find it with:
   ```bash
   ls /dev/cu.usbmodem*
   ```

5. **Monitor output**:
   ```bash
   idf.py monitor
   ```
   
   Press `Ctrl+]` to exit the monitor.

## Expected Behavior

- The onboard LED will blink on and off every 1 second
- Serial monitor will display ESP_LOG messages showing "LED ON" and "LED OFF"
- Baud rate: 115200

## Troubleshooting

1. **Build errors**: Make sure ESP-IDF is properly installed and sourced
2. **Flash errors**: Check the USB connection and port permissions
3. **No LED blinking**: Verify the board is a Seeed ESP32-C3 with LED on GPIO2

## Project Structure

```
03espIdfArduinoLib/
├── CMakeLists.txt          # Main project CMake file
├── sdkconfig.defaults      # Default ESP-IDF configuration
├── partitions.csv          # Custom partition table
├── main/
│   ├── CMakeLists.txt      # Main component CMake file
│   └── main.cpp            # Arduino-style main code with ESP-IDF
├── build_and_flash.sh      # Automated build and flash script
└── README.md               # This file
```

## Configuration Details

- **Target**: ESP32-C3
- **Flash size**: 4MB
- **Native ESP-IDF**: With Arduino-style function wrappers
- **USB Serial/JTAG**: Enabled for easy debugging
- **CPU frequency**: 160MHz
- **Log level**: INFO

## Advantages over Full Arduino Framework

1. **Smaller footprint**: No Arduino framework overhead
2. **Better performance**: Direct ESP-IDF calls
3. **Full ESP-IDF access**: Can use any ESP-IDF feature
4. **Familiar syntax**: Arduino-style functions for ease of use
5. **Educational**: Learn ESP-IDF while using familiar patterns
