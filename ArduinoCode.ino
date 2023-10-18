#include <WiFi.h> //Library for ESP32 WiFi module
#include <WebServer.h> //EPS32 WebServer
#include <ArduinoJson.h> //Json document type for Webserver
#include "EmonLib.h" //EmonLib for AC Sine calculation

const char* ssid = "WiFi-name"; //replace with WiFi name
const char* password = "WiFi-password"; //replace with WiFi password

const int ctPins[] = {32, 33, 34, 35, 36, 39}; // Pins for the CT sensors
const float emonCalibration[] = {0.00152, 0.00152, 0.00152, 0.00152, 0.00152, 0.0}; // Calibration factors for each CT, only 5 CTs used
const int ctNumberTurns[] = {2000, 2000, 2000, 2000, 2000, 2000}; // Turns ratios for each CT

EnergyMonitor emon[6]; // Create an array of EnergyMonitor objects for six CTs
WebServer server(80);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("WLAN connecting...");
  }
  Serial.println("WLAN connected");

  // Initialize EnergyMonitor objects for each CT
  for (int i = 0; i < 6; i++) {
    emon[i].current(ctPins[i], ctNumberTurns[i]);
  }

  server.on("/", HTTP_GET, handleRequest);
  server.begin();
}

void loop() {
  server.handleClient();
}

void handleRequest() {
  // Create a JSON object for multiple CTs
  DynamicJsonDocument jsonDoc(256);
  for (int i = 0; i < 6; i++) {
    // Calculate current for each CT using its individual calibration factor
    float current = emon[i].calcIrms(1480) * emonCalibration[i]; // Number of samples
    jsonDoc["ct_" + String(i)] = current;
  }


  String jsonString;
  serializeJson(jsonDoc, jsonString);

  server.send(200, "application/json", jsonString);
} 
