const int blueLed = 1;
const int whiteLed = 2;
const int redLed = 4;
//const int switchPin = 2;


void setup() {
  // put your setup code here, to run once:
  pinMode(whiteLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  pinMode(redLed, OUTPUT);
}


void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(blueLed, HIGH);
  delay(150);
  digitalWrite(redLed, LOW);
  delay(300);

  digitalWrite(whiteLed, HIGH);
  delay(150);
  digitalWrite(blueLed, LOW);
  delay(300);

  digitalWrite(redLed, HIGH);
  delay(150);
  digitalWrite(whiteLed, LOW);
  delay(300);
}
