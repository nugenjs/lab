#include <Arduino.h>
#include <WiFi.h>
#include "esp_log.h"
#include "mqtt_client.h"

#define OFFCMD_PIN 10
#define DOWNCMD_PIN 9
#define UPCMD_PIN 8
#define ONCMD_PIN 20
#define BTN_PRESS_DURATION 1000

static const char *TAG = "ESP32C3_MQTT";

// Forward declarations
void handleMqttCommand(String command);
void publishStatus(String status);
void connectMqtt();
void pressButton(String btnName);

extern "C" void app_main() {
  ESP_LOGI(TAG, "Starting app_main");
  initArduino();     // Bring up Arduino runtime inside ESP-IDF
  ESP_LOGI(TAG, "Arduino runtime initialized");
  setup();           // Call your existing Arduino setup()
  ESP_LOGI(TAG, "Setup completed, entering loop");
  for (;;) {         // Cooperatively run loop()
    loop();
    vTaskDelay(1);   // yield to FreeRTOS
  }
}

// ==== Wi-Fi credentials ====
const char* WIFI_SSID     = "iot";
const char* WIFI_PASSWORD = "WIFI_PASSWORD";

// ==== MQTT credentials ====
// const char* MQTT_BROKER = "192.168.9.216";  // Direct IP to local broker
const char* MQTT_BROKER = "mqtt.io";  // Custom hostname on local router
// const char* MQTT_BROKER = "test.mosquitto.org";  // Public broker for testing
const int MQTT_PORT = 1883;
const char* MQTT_CLIENT_ID = "esp32c3_bed_controller";
const char* MQTT_TOPIC_COMMAND = "bed/command";
const char* MQTT_TOPIC_STATUS = "bed/status";
// const char* MQTT_USERNAME = "MQTT_USER";  // Add if your broker requires auth
// const char* MQTT_PASSWORD = "MQTT_PASS";  // Add if your broker requires auth
const char* MQTT_USERNAME = "";  // Add if your broker requires auth
const char* MQTT_PASSWORD = "";  // Add if your broker requires auth


// ==== MQTT client setup ====
esp_mqtt_client_handle_t mqttClient;

// MQTT event handler
static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
  esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t)event_data;
  
  switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
      ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
      // Subscribe to command topic
      esp_mqtt_client_subscribe(mqttClient, MQTT_TOPIC_COMMAND, 0);
      ESP_LOGI(TAG, "Subscribed to topic: %s", MQTT_TOPIC_COMMAND);
      
      // Publish initial status
      publishStatus("ESP32C3 bed controller online");
      break;
      
    case MQTT_EVENT_DISCONNECTED:
      ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
      break;
      
    case MQTT_EVENT_SUBSCRIBED:
      ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
      break;
      
    case MQTT_EVENT_UNSUBSCRIBED:
      ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
      break;
      
    case MQTT_EVENT_PUBLISHED:
      ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
      break;
      
    case MQTT_EVENT_DATA:
      {
        ESP_LOGI(TAG, "MQTT_EVENT_DATA");
        // Convert topic and payload to strings
        String topic = String(event->topic).substring(0, event->topic_len);
        String message = String((char*)event->data).substring(0, event->data_len);
        message.trim();
        message.toLowerCase();
        
        ESP_LOGI(TAG, "MQTT message received on topic '%s': %s", topic.c_str(), message.c_str());
        
        // Handle the command
        if (topic == MQTT_TOPIC_COMMAND) {
          handleMqttCommand(message);
        }
      }
      break;
      
    case MQTT_EVENT_ERROR:
      ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
      break;
      
    case MQTT_EVENT_BEFORE_CONNECT:
      ESP_LOGI(TAG, "MQTT_EVENT_BEFORE_CONNECT");
      break;
      
    case MQTT_EVENT_DELETED:
      ESP_LOGI(TAG, "MQTT_EVENT_DELETED");
      break;
      
    case MQTT_USER_EVENT:
      ESP_LOGI(TAG, "MQTT_USER_EVENT");
      break;
      
    case MQTT_EVENT_ANY:
    default:
      ESP_LOGI(TAG, "Other event id:%d", event->event_id);
      break;
  }
}

void handleMqttCommand(String command) {
  ESP_LOGI(TAG, "Processing MQTT command: %s", command.c_str());
  
  if (command == "on" || command == "ON") {
    pressButton("ON");
    publishStatus("ON pressed");
  } else if (command == "off" || command == "OFF") {
    pressButton("OFF");
    publishStatus("OFF pressed");
  } else if (command == "up" || command == "UP") {
    pressButton("UP");
    publishStatus("UP pressed");
  } else if (command == "down" || command == "DOWN") {
    pressButton("DOWN");
    publishStatus("DOWN pressed");
  } else if (command == "unit" || command == "UNIT") {
    pressButton("unit");
    publishStatus("UNIT test pressed");
  } else {
    ESP_LOGW(TAG, "Unknown MQTT command: %s", command.c_str());
    publishStatus("Unknown command: " + command);
  }
}

void publishStatus(String status) {
  String statusMsg = "{\"status\":\"" + status + "\",\"timestamp\":" + String(millis()) + "}";
  if (mqttClient) {
    int msg_id = esp_mqtt_client_publish(mqttClient, MQTT_TOPIC_STATUS, statusMsg.c_str(), 0, 0, 0);
    ESP_LOGI(TAG, "Published status (msg_id=%d): %s", msg_id, statusMsg.c_str());
  }
}

// Takes in name of bttn to press
void pressButton(String btnName) {
  // digitalWrite(OFFCMD_PIN, on ? HIGH : LOW);

  if (btnName == "ON") {
    ESP_LOGI(TAG, "Pressing ON");
    // pinMode(ONCMD_PIN, OUTPUT);     // GPIO 20
    digitalWrite(ONCMD_PIN, HIGH);
    delay(BTN_PRESS_DURATION);
    digitalWrite(ONCMD_PIN, LOW);
    ESP_LOGI(TAG, "Released ON");
  } else if (btnName == "OFF") {

    ESP_LOGI(TAG, "Pressing OFF");
    // pinMode(OFFCMD_PIN, OUTPUT);     // GPIO 10
    digitalWrite(OFFCMD_PIN, HIGH);
    delay(BTN_PRESS_DURATION * 2);
    digitalWrite(OFFCMD_PIN, LOW);
    ESP_LOGI(TAG, "Released OFF");
  } else if (btnName == "UP") {

    ESP_LOGI(TAG, "Pressing UP");
    // pinMode(UPCMD_PIN, OUTPUT);     // GPIO 8
    digitalWrite(UPCMD_PIN, HIGH);
    delay(BTN_PRESS_DURATION);
    digitalWrite(UPCMD_PIN, LOW);
    ESP_LOGI(TAG, "Released UP");
  } else if (btnName == "DOWN") {
    ESP_LOGI(TAG, "Pressing DOWN");
    // pinMode(DOWNCMD_PIN, OUTPUT);     // GPIO 9
    digitalWrite(DOWNCMD_PIN, HIGH);
    delay(BTN_PRESS_DURATION);
    digitalWrite(DOWNCMD_PIN, LOW);
    ESP_LOGI(TAG, "Released DOWN");
  } else if (btnName == "unit") {
    ESP_LOGI(TAG, "Pressing UP");
    ESP_LOGI(TAG, "Pressing DOWN");
    // pinMode(UPCMD_PIN, OUTPUT);     // GPIO 9
    // pinMode(DOWNCMD_PIN, OUTPUT);     // GPIO 9
    digitalWrite(UPCMD_PIN, HIGH);
    digitalWrite(DOWNCMD_PIN, HIGH);
    delay(BTN_PRESS_DURATION);
    digitalWrite(UPCMD_PIN, LOW);
    digitalWrite(DOWNCMD_PIN, LOW);
    ESP_LOGI(TAG, "Released UP");
    ESP_LOGI(TAG, "Released DOWN");
  } else {
    ESP_LOGW(TAG, "Unknown button name: %s", btnName.c_str());
  }
}

void connectMqtt() {
  ESP_LOGI(TAG, "Initializing MQTT client for %s:%d", MQTT_BROKER, MQTT_PORT);
  
  // Build MQTT broker URI
  String broker_uri = "mqtt://" + String(MQTT_BROKER) + ":" + String(MQTT_PORT);
  
  esp_mqtt_client_config_t mqtt_cfg = {};
  mqtt_cfg.broker.address.uri = broker_uri.c_str();
  mqtt_cfg.credentials.client_id = MQTT_CLIENT_ID;
  
  // Add credentials if provided
  if (strlen(MQTT_USERNAME) > 0) {
    mqtt_cfg.credentials.username = MQTT_USERNAME;
    mqtt_cfg.credentials.authentication.password = MQTT_PASSWORD;
  }
  
  mqttClient = esp_mqtt_client_init(&mqtt_cfg);
  if (mqttClient == NULL) {
    ESP_LOGE(TAG, "Failed to initialize MQTT client");
    return;
  }
  
  esp_mqtt_client_register_event(mqttClient, MQTT_EVENT_ANY, mqtt_event_handler, NULL);
  esp_mqtt_client_start(mqttClient);
  
  ESP_LOGI(TAG, "MQTT client started");
}

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.setHostname("coolbed-iot");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  ESP_LOGI(TAG, "Connecting to Wi-Fi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    ESP_LOGI(TAG, ".");
    if (millis() - start > 30000) { // 30s timeout, then retry
      ESP_LOGI(TAG, "\nRetrying Wi-Fi...");
      WiFi.disconnect();
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      start = millis();
    }
  }
  
  ESP_LOGI(TAG, "Wi-Fi connected!");
  ESP_LOGI(TAG, "IP address: %s", WiFi.localIP().toString().c_str());
  ESP_LOGI(TAG, "Gateway: %s", WiFi.gatewayIP().toString().c_str());
  ESP_LOGI(TAG, "DNS: %s", WiFi.dnsIP().toString().c_str());
  ESP_LOGI(TAG, "Subnet: %s", WiFi.subnetMask().toString().c_str());
  
  // Test basic network connectivity to MQTT broker
  ESP_LOGI(TAG, "Testing TCP connectivity to MQTT broker...");
  WiFiClient testClient;
  if (testClient.connect(MQTT_BROKER, MQTT_PORT)) {
    ESP_LOGI(TAG, "TCP connection to %s:%d SUCCESS!", MQTT_BROKER, MQTT_PORT);
    testClient.stop();
  } else {
    ESP_LOGE(TAG, "TCP connection to %s:%d FAILED!", MQTT_BROKER, MQTT_PORT);
    ESP_LOGE(TAG, "This indicates a network/firewall issue, not an MQTT protocol issue");
  }
}

void setup() {
  // Initialize all GPIO pins immediately on boot
  pinMode(DOWNCMD_PIN, OUTPUT);   // GPIO 9
  digitalWrite(DOWNCMD_PIN, LOW);
  
  pinMode(UPCMD_PIN, OUTPUT);     // GPIO 8
  digitalWrite(UPCMD_PIN, LOW);
  
  pinMode(OFFCMD_PIN, OUTPUT);    // GPIO 10
  digitalWrite(OFFCMD_PIN, LOW);
  

  pinMode(ONCMD_PIN, OUTPUT);    // GPIO 10
  digitalWrite(ONCMD_PIN, LOW);

  // // Special handling for GPIO20 - it might need explicit GPIO mode setting
  // Serial.println("Initializing GPIO20...");
  // // Try ESP-IDF method first to set GPIO20 as GPIO function
  // ESP_LOGI(TAG, "Setting GPIO20 as GPIO function");
  // // Use Arduino pinMode - this should call the underlying ESP-IDF functions
  // pinMode(ONCMD_PIN, OUTPUT);     // GPIO 20
  // // Force multiple writes to ensure it takes
  // for(int i = 0; i < 3; i++) {
  //   digitalWrite(ONCMD_PIN, LOW);
  //   delay(10);
  // }
  // ESP_LOGI(TAG, "GPIO20 initialized, current state: %s", digitalRead(ONCMD_PIN) ? "HIGH" : "LOW");
  
  // Serial.begin(115200);
  // delay(200);
  pinMode(ONCMD_PIN, OUTPUT);
  
  ESP_LOGI(TAG, "All GPIO pins initialized to LOW");
  
  // Check pin states after initialization
  ESP_LOGI(TAG, "PIN STATES AFTER INIT:");
  ESP_LOGI(TAG, "  GPIO8 (UP): %s", digitalRead(UPCMD_PIN) ? "HIGH" : "LOW");
  ESP_LOGI(TAG, "  GPIO9 (DOWN): %s", digitalRead(DOWNCMD_PIN) ? "HIGH" : "LOW");
  ESP_LOGI(TAG, "  GPIO10 (OFF): %s", digitalRead(OFFCMD_PIN) ? "HIGH" : "LOW");
  ESP_LOGI(TAG, "  GPIO20 (ON): %s", digitalRead(ONCMD_PIN) ? "HIGH" : "LOW");

  // pinMode(OFFCMD_PIN, OUTPUT);
  // pressButton(false); // start off

  connectWiFi();
  
  // Connect to MQTT broker
  connectMqtt();

  ESP_LOGI(TAG, "MQTT bed controller started");
  ESP_LOGI(TAG, "Send commands to MQTT topic: %s", MQTT_TOPIC_COMMAND);
  ESP_LOGI(TAG, "Status updates published to: %s", MQTT_TOPIC_STATUS);
  ESP_LOGI(TAG, "Supported commands: ON, OFF, UP, DOWN, UNIT");

  // pinMode(ONCMD_PIN, OUTPUT);
}

void loop() {
  // Connection watchdog
  static unsigned long lastCheck = 0;
  static unsigned long lastBootCheck = 0;
  
  if (millis() - lastCheck > 10000) { // every 10s
    lastCheck = millis();
    
    // Check Wi-Fi connection
    if (WiFi.status() != WL_CONNECTED) {
      ESP_LOGW(TAG, "Wi-Fi lost. Reconnecting...");
      connectWiFi();
    }
  }

  // Monitor all GPIO pin states every 30 seconds
  if (millis() - lastBootCheck > 30000) {
    ESP_LOGI(TAG, "=== STATUS REPORT ===");
    ESP_LOGI(TAG, "WiFi: %s", WiFi.status() == WL_CONNECTED ? "Connected" : "Disconnected");
    ESP_LOGI(TAG, "GPIO8 (UP): %s", digitalRead(UPCMD_PIN) ? "HIGH" : "LOW");
    ESP_LOGI(TAG, "GPIO9 (DOWN): %s", digitalRead(DOWNCMD_PIN) ? "HIGH" : "LOW");
    ESP_LOGI(TAG, "GPIO10 (OFF): %s", digitalRead(OFFCMD_PIN) ? "HIGH" : "LOW");
    ESP_LOGI(TAG, "GPIO20 (ON): %s", digitalRead(ONCMD_PIN) ? "HIGH" : "LOW");
    ESP_LOGI(TAG, "====================");
    
    // Publish periodic status if MQTT client exists
    if (mqttClient) {
      publishStatus("Periodic status update");
    }
    
    lastBootCheck = millis();
  }
}