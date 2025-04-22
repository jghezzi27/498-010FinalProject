#include "General.h"

void ToActive() {
  digitalWrite(ActivePin, HIGH);
  Serial.println("To Active");
  State = ACTIVE;
}

void ToApproved() {
  digitalWrite(ActivePin, LOW);
  Serial.println("To Approved");
  State = APPROVED;
  startTime = millis();
}
