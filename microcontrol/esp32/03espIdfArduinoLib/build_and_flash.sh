#!/bin/bash

# ESP32-C3 Arduino Blink - Build and Flash Script
# This script automates the build and flash process for the ESP32-C3 Arduino blink project

echo "ESP32-C3 Arduino Blink - Build and Flash Script"
echo "================================================"

# Check if ESP-IDF is sourced
if [ -z "$IDF_PATH" ]; then
    echo "Error: ESP-IDF environment not found!"
    echo "Please source ESP-IDF first:"
    echo "  . \$HOME/esp/esp-idf/export.sh"
    exit 1
fi

echo "ESP-IDF Path: $IDF_PATH"

# Set target to ESP32-C3
echo "Setting target to ESP32-C3..."
idf.py set-target esp32c3

if [ $? -ne 0 ]; then
    echo "Error: Failed to set target to ESP32-C3"
    exit 1
fi

# Build the project
echo "Building project..."
idf.py build

if [ $? -ne 0 ]; then
    echo "Error: Build failed"
    exit 1
fi

echo "Build successful!"

# Check if a port argument was provided
if [ $# -eq 1 ]; then
    PORT=$1
    echo "Using specified port: $PORT"
    
    # Flash and monitor
    echo "Flashing to $PORT and starting monitor..."
    idf.py -p $PORT flash monitor
else
    echo "No port specified. Available ports:"
    ls /dev/cu.usbmodem* 2>/dev/null || echo "No USB modem devices found"
    echo ""
    echo "To flash, run:"
    echo "  idf.py -p /dev/cu.usbmodem[YOUR_PORT] flash monitor"
    echo ""
    echo "Or run this script with a port:"
    echo "  ./build_and_flash.sh /dev/cu.usbmodem[YOUR_PORT]"
fi
