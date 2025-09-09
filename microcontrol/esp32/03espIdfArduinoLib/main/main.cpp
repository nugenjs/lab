/**
 * ESP32-C3 Arduino Blink Example for Seeed ESP32-C3
 * 
 * This example demonstrates how to use ESP-IDF with Arduino component
 * to blink the onboard LED on a Seeed ESP32-C3 board.
 * 
 * LED is connected to GPIO10
 */

#include <stdio.h>
#include "Arduino.h"
#include "esp_log.h"

static const char *TAG = "ESP32C3_BLINK";

// Define the LED pin for Seeed ESP32-C3
#define LED_PIN 10

// Define blink interval in milliseconds
#define BLINK_INTERVAL 1000

extern "C" void app_main()
{
    // Initialize Arduino
    initArduino();
    
    ESP_LOGI(TAG, "ESP32-C3 Arduino Blink Starting...");
    ESP_LOGI(TAG, "LED on GPIO%d will blink every %d ms", LED_PIN, BLINK_INTERVAL);
    
    // Set LED pin as output (Arduino-style)
    pinMode(LED_PIN, OUTPUT);
    
    while(1) {
        // Turn LED on
        digitalWrite(LED_PIN, HIGH);
        ESP_LOGI(TAG, "LED ON");
        delay(BLINK_INTERVAL);

        ESP_LOGI(TAG, "LED will turn off in %d ms", BLINK_INTERVAL);

        // Turn LED off
        digitalWrite(LED_PIN, LOW);
        ESP_LOGI(TAG, "LED OFF");
        delay(BLINK_INTERVAL);
    }
}
