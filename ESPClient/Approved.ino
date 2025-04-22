#include "General.h"

const unsigned long ApprovedDuration = 20000;

void DoApproved() {
  // Switch state if Approved Duration has elapsed
  if (millis() - startTime >= ApprovedDuration) {
    // Later, switch to resting if IR Sensor is LOW, Active if IR Sensor is HIGH
    ToActive();
    return;
  }

  // See if button has been pressed to change lock state
  int buttonState = digitalRead(ButtonPin);

  if (buttonState == HIGH) {
    unsigned long buttonTime = millis();
    switch (lockState) {
      case LOCKED:
        Serial.println("Unlocking");
        lockState = UNLOCKED;
        digitalWrite(LockPin, HIGH);

        // Do the "unlocking" (light up the green light, for now)
        while (millis() - buttonTime <= 5000) {
          delay(300);
        }
        break;

      case UNLOCKED:
        Serial.println("Locking");
        lockState = LOCKED;
        digitalWrite(LockPin, LOW);
        // Do the "locking" (light up the green light, for now)
        while (millis() - buttonTime <= 5000) {
          delay(300);
        }
        break;
    }
  }
}
