// Functions for Active System State
// System is awake and is sending images to the server

#include "General.h"

const unsigned long ImageDelay = 5000;

void sendImageAndLockIdToServer(camera_fb_t* fb) {
  // Prepare the HTTP client configuration
  esp_http_client_config_t config = {
    .url = serverName, // Flask server URL
  };

  esp_http_client_handle_t client = esp_http_client_init(&config);

  esp_http_client_set_method(client, HTTP_METHOD_POST);

  // Prepare the multipart form data for the image and lock_id
  String boundary = "----ESP32Boundary";
  String contentType = "multipart/form-data; boundary=" + boundary;

  // Set the headers for the request
  esp_http_client_set_header(client, "Content-Type", contentType.c_str());

  // Start constructing the body of the request
  String body = "--" + boundary + "\r\n";
  body += "Content-Disposition: form-data; name=\"lock_id\"\r\n\r\n" + String(lock_id) + "\r\n";
  body += "--" + boundary + "\r\n";
  body += "Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n";
  body += "Content-Type: image/jpeg\r\n\r\n";

  // Append the image data (binary part of the form)
  body += String((const char*)fb->buf, fb->len);  // Add the image bytes here
  
  // End the multipart message with the boundary
  body += "\r\n--" + boundary + "--\r\n";

  // Send the full body (lock_id and image data) in a single POST request
  esp_http_client_set_post_field(client, body.c_str(), body.length());

  // Perform the HTTP request
  esp_http_client_perform(client);

  // Check the response code
  int httpResponseCode = esp_http_client_get_status_code(client);
  if (httpResponseCode > 0) {
    Serial.print("Server Response Code: ");
    Serial.println(httpResponseCode);

    int64_t lenRes = esp_http_client_get_content_length(client);
    switch (lenRes) {
      case 19:
        Serial.println("Failure");
        break;
      case 20:
        Serial.println("Error");
        break;
      case 21:
        Serial.println("No Face Found");
        break;
      case 22:
        Serial.println("Success!");
        ToApproved();
        break;

      default:
        Serial.println("Weird Response!");
    }
  } else {
    Serial.println("Failed to send image and lock_id to server");
  }

  // Clean up the client after sending the data
  esp_http_client_cleanup(client);
}


void DoActive() {
  // Capture an image from the camera
  //digitalWrite(flashPin, HIGH);
  //delay(100);
  camera_fb_t* fb = esp_camera_fb_get();
  //digitalWrite(flashPin, LOW);
 
  if (!fb) {
    Serial.println("Capture failed");
    return;
  }

  // Send the captured image and lock_id to the Flask server
  sendImageAndLockIdToServer(fb);

  // Free the camera buffer
  esp_camera_fb_return(fb);
  if (State == ACTIVE) {
    delay(ImageDelay);
  }
}
