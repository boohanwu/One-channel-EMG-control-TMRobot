void setup()
{
  Serial.begin(115200); 
}

void loop()
{
  int val1 = analogRead(A0);

  Serial.print(val1);
  Serial.print("\n"); 
  delay(10);
}
