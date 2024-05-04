#define inPin0 0


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println();
}


void loop() {
  // put your main code here, to run repeatedly:
  int pinRead0 = analogRead(inPin0);
  float pVolt0 = pinRead0;
  Serial.print(pVolt0);
  Serial.println();
   
  delay(300);
}
