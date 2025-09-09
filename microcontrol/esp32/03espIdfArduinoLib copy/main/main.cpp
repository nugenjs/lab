/**
 * ESP32-C3 Arduino-style Blink Example for Seeed ESP32-C3
 * 
 * This example demonstrates how to use ESP-IDF with Arduino-style functions
 * to blink the onboard LED on a Seeed ESP32-C3 board.
 * 
 * Seeed ESP32-C3 onboard LED is connected to GPIO2
 */

#include <stdio.h>
#include <unistd.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "ESP32C3_BLINK";

// Define the LED pin for Seeed ESP32-C3
#define LED_PIN GPIO_NUM_10

// Define blink interval in milliseconds
#define BLINK_INTERVAL 1000

// Arduino-style functions implemented using ESP-IDF
void pinMode(gpio_num_t pin, gpio_mode_t mode) {
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = mode;
    io_conf.pin_bit_mask = (1ULL << pin);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);
}

void digitalWrite(gpio_num_t pin, uint32_t val) {
    gpio_set_level(pin, val);
}

void delay(uint32_t ms) {
    vTaskDelay(ms / portTICK_PERIOD_MS);
}

extern "C" void app_main()
{
    ESP_LOGI(TAG, "ESP32-C3 Arduino-style Blink Starting...");
    ESP_LOGI(TAG, "Seeed ESP32-C3 onboard LED will blink every %d ms", BLINK_INTERVAL);
    
    // Set LED pin as output (Arduino-style)
    pinMode(LED_PIN, GPIO_MODE_OUTPUT);
    
    while(1) {
        // Turn LED on
        digitalWrite(LED_PIN, 1);
        ESP_LOGI(TAG, "LED ON");
        delay(BLINK_INTERVAL);
        
        // Turn LED off
        digitalWrite(LED_PIN, 0);
        ESP_LOGI(TAG, "LED OFF");
        delay(BLINK_INTERVAL);
    }
}
