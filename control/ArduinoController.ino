void setup() {
  Serial.begin(9600);
}

void loop() {
  bool btn1 = digitalRead(2);
  bool btn2 = digitalRead(3);
  bool joybtn = not digitalRead(4);
  int axis0 = analogRead(6);
  int axis1 = analogRead(7);

  Serial.print("$START ");
  Serial.print(btn1);
  Serial.print(" ");
  Serial.print(btn2);
  Serial.print(" ");
  Serial.print(joybtn);
  Serial.print(" ");
  Serial.print(axis0);
  Serial.print(" ");
  Serial.print(axis1);
  Serial.println(" $END");
  

  delay(10);
}
