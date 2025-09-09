#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

#define LED_PIN 20 // GPIO 20

// ==== Wi-Fi credentials ====
// const char* WIFI_SSID     = "iot";
// const char* WIFI_PASSWORD = "thepasswordspecificallyforiot";
const char* WIFI_SSID     = "iot";
const char* WIFI_PASSWORD = "WIFI_PASSWORD";


// ==== LED pin setup ====
// Try to use LED_BUILTIN if available; otherwise use GPIO 2 as a common default.
// #ifndef LED_BUILTIN
//   #define LED_BUILTIN 2
// #endif
// const int LED_PIN = LED_BUILTIN;

// ==== HTTP server on port 80 ====
WebServer server(80);

// Utility: set CORS headers (handy when calling from a browser/fetch)
void setCommonHeaders() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}

// Handlers
void handleRoot() {
  setCommonHeaders();
  String msg = F("{\"endpoints\":[\"/led/on\",\"/led/off\",\"/led?state=on|off\"],\"status\":\"ok\"}");
  server.send(200, "application/json", msg);
}

void handleOptions() { // preflight for CORS
  setCommonHeaders();
  server.send(204); // No Content
}

void setLed(bool on) {
  digitalWrite(LED_PIN, on ? HIGH : LOW);

  if (on) {
    Serial.println("LED is ON");
    delay(2000);
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("LED is OFF");
  }
}

void handleLedToggleExplicit(bool turnOn) {
  setLed(turnOn);
  setCommonHeaders();
  server.send(200, "application/json",
              String("{\"led\":\"") + (turnOn ? "on" : "off") + "\"}");
}

void handleLedQuery() {
  // /led?state=on or /led?state=off
  if (!server.hasArg("state")) {
    setCommonHeaders();
    server.send(400, "application/json",
                "{\"error\":\"missing 'state' query param (use on|off)\"}");
    return;
  }
  String s = server.arg("state");
  s.toLowerCase();

  if (s == "on") {
    handleLedToggleExplicit(true);
  } else if (s == "off") {
    handleLedToggleExplicit(false);
  } else {
    setCommonHeaders();
    server.send(400, "application/json",
                "{\"error\":\"invalid state (use on|off)\"}");
  }
}

void handleNotFound() {
  setCommonHeaders();
  server.send(404, "application/json",
              "{\"error\":\"not found\"}");
}

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.setHostname("coolbed-iot");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to Wi-Fi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
    if (millis() - start > 30000) { // 30s timeout, then retry
      Serial.println("\nRetrying Wi-Fi...");
      WiFi.disconnect();
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      start = millis();
    }
  }
  Serial.println("\nWi-Fi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(LED_PIN, OUTPUT);
  setLed(false); // start off

  connectWiFi();

  // Routes
  server.on("/", HTTP_GET, handleRoot);
  server.on("/led", HTTP_GET, handleLedQuery);
  server.on("/led/on", HTTP_GET, []() { handleLedToggleExplicit(true); });
  server.on("/led/off", HTTP_GET, []() { handleLedToggleExplicit(false); });

  // CORS preflight (OPTIONS)
  server.on("/", HTTP_OPTIONS, handleOptions);
  server.on("/led", HTTP_OPTIONS, handleOptions);
  server.on("/led/on", HTTP_OPTIONS, handleOptions);
  server.on("/led/off", HTTP_OPTIONS, handleOptions);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
  Serial.println("Try:");
  Serial.println("  http://<device-ip>/");
  Serial.println("  http://<device-ip>/led/on");
  Serial.println("  http://<device-ip>/led/off");
  Serial.println("  http://<device-ip>/led?state=on");
}

void loop() {
  server.handleClient();

  // Optional: auto-reconnect watchdog
  static unsigned long lastCheck = 0;
  if (millis() - lastCheck > 10000) { // every 10s
    lastCheck = millis();
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("Wi-Fi lost. Reconnecting...");
      connectWiFi();
    }
  }
}