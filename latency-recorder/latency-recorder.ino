const int whiteLed = 3;
//const int switchPin = 2;


void setup() {
  // put your setup code here, to run once:
  pinMode(whiteLed, OUTPUT);
}


void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(whiteLed, LOW);
  delay(500);
  digitalWrite(whiteLed, HIGH);
  delay(500);

}
