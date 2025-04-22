#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <Base64.h>
#include "esp_camera.h"
#include "esp_http_client.h"
#include "ArduinoJson.h"
#include "General.h"

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

#define flashPin 4

// Define your Wi-Fi credentials
const char* ssid = ""; // Fill this in yourself
const char* password = ""; // Fill this in yourself

// Define the server URL
const char* serverName = "" // HTTP POST endpoint; Fill this in yourself
const int ButtonPin = 12;
const int LockPin = 13;
const int ActivePin = 15;

// Define lock_id
String lock_id = "lock1";

// Define Server/Lock State
SystemState State = ACTIVE;
LockState lockState = UNLOCKED;

// Define start time (for various states)
unsigned long startTime = 0;


void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");


  pinMode(flashPin, OUTPUT);
  pinMode(ButtonPin, INPUT);
  pinMode(LockPin, OUTPUT);
  pinMode(ActivePin, OUTPUT);


  // Config
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_XGA;
  config.pixel_format = PIXFORMAT_JPEG;  // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 2;
  config.grab_mode = CAMERA_GRAB_LATEST;

  // Initialize the camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera initialization failed with error 0x%x", err);
    return;
  }

  Serial.println("Camera initialized");

  digitalWrite(LockPin, HIGH);
  digitalWrite(ActivePin, HIGH);
}


void loop() {
  switch (State) {
    case ACTIVE:
      DoActive();
      break;

    case APPROVED:
      DoApproved();
      break;
  }
}
