# BedAC
ESP32C3 hooked up to a mattress water cooler, to make it controllable through MQTT.

### Settings
Using arduino library instead of pure FreeRTOS for easy dev\
Setting 
CONFIG_FREERTOS_HZ=1000 in ./sdconfig due to using arduino library\
CONFIG_DIAG_USE_EXTERNAL_LOG_WRAP=y fixes
CONFIG_BT_ENABLED=y
CONFIG_BT_BLE_50_FEATURES_SUPPORTED=n
CONFIG_BT_BLE_42_FEATURES_SUPPORTED=y
CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_80=y
CONFIG_FREERTOS_HZ=1000