const int forPin = 13;
const int backPin = 12;
int ledPin = 7;                // choose the pin for the LED
int inputPin = 8;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
int i = 0;

void setup() {
  pinMode(forPin, OUTPUT);
  pinMode(backPin, OUTPUT);
  pinMode(ledPin, OUTPUT);      // declare LED as output
  pinMode(inputPin, INPUT);     // declare sensor as input
  Serial.begin(9600);
}

void loop() {

    val = digitalRead(inputPin);  // read input value
  
  if (val == HIGH)  // check if the input is HIGH
  {            
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (i % 1000 == 0) {
      Serial.println("HIGH");
      i = 1;
    }
    digitalWrite(forPin, HIGH);
    delay(3000);
    digitalWrite(forPin, LOW);
    delay(2000);
    digitalWrite(backPin, HIGH);
    delay(3000);
    digitalWrite(backPin, LOW);
    delay(2000);

    if (pirState == LOW) 
    {
      Serial.println("Motion detected!"); // print on output change
      pirState = HIGH;
    }
  } 
  else 
  {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (i % 1000000 == 0) {
      Serial.println("LOW");
      i = 1;
    }
    if (pirState == HIGH)
  {
      Serial.println("Motion ended!");  // print on output change
      pirState = LOW;
    }
  }
  i++;
}
