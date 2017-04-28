#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <gpio.h>

#define CLOCK_DELAY 30
#define WIFI_TYPE 1


char* ssid = "HOME-5140-2.4";
char* password = "U9U4EL7CACPPEV3R";

char* ssid_UI = "IllinoisNet_Guest";

String sensor_payload;

void setup() {

  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D1,OUTPUT); // ALE output
  pinMode(D2,INPUT);  // Pin D2 is used for serial input
  pinMode(D3,OUTPUT); // Enable
  pinMode(D4,OUTPUT); // Pin D4 is Clock output
  pinMode(D5,OUTPUT); // Reset
  pinMode(D6,INPUT_PULLUP); // READY bit
  pinMode(D7,INPUT_PULLUP); // IR1
  pinMode(D8,INPUT_PULLUP); // IR2
  
  Serial.println("Connecting");
  
  
  digitalWrite(LED_BUILTIN, HIGH);
  ConnectWiFi();
  //tone(D7,32); // IR Emitter 1 Square Wave
  //tone(D8,36000); // IR Emitter 2 Square Wave
  // analogWrite(D7,2);
  //analogWriteFreq(20);

  //attachInterrupt(digitalPinToInterrupt(D7),ir1);
  //attachInterrupt(digitalPinToInterrupt(D8),ir2);
    
}

void loop() {
  uint8_t CurrentSensorValue;
  sensor_payload = "=";
  
  if(WiFi.status()!=WL_CONNECTED)
  {
    ConnectWiFi();
    Serial.println("Lost Wireless connectivity");
  }

  
  //Serial.println("HERE");

  // INIT IS DONE!
  //Serial.println("HERE");
  // Get data
  for(int i = 0; i < 8; i++)
  {
    
    for(int j = 0 ; j < 8; j++)
    {
        if(i==0 && j==0)
        {   
          digitalWrite(D5, LOW);    // Reset goes LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D3, HIGH);    // ENABLE goes HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, LOW);    // CLOCK GOES LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D5, HIGH);    // Reset goes HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D3, LOW);    // ENABLE goes LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, LOW);    // CLOCK GOES LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D3, HIGH);    // ENABLE goes HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, LOW);    // CLOCK GOES LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D3, LOW);    // ENABLE goes LOW
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
          delayMicroseconds(CLOCK_DELAY);
          digitalWrite(D4, LOW);    // CLOCK GOES LOW
          delayMicroseconds(CLOCK_DELAY);
        }

        digitalWrite(D1, HIGH);    // ALE goes HIGH
        delayMicroseconds(CLOCK_DELAY);
        digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
        delayMicroseconds(CLOCK_DELAY);
        digitalWrite(D4, LOW);    // CLOCK GOES LOW
        delayMicroseconds(CLOCK_DELAY);
//        digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
//        delayMicroseconds(CLOCK_DELAY);
//        digitalWrite(D4, LOW);    // CLOCK GOES LOW
//        delayMicroseconds(CLOCK_DELAY);
        digitalWrite(D1, LOW);    // ALE goes LOW
        delayMicroseconds(CLOCK_DELAY);
        digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
        delayMicroseconds(CLOCK_DELAY);
        digitalWrite(D4, LOW);    // CLOCK GOES LOW
        delayMicroseconds(CLOCK_DELAY);

      CurrentSensorValue = 0;
      while(digitalRead(D6)!=HIGH)
      {
        //Serial.println("HERE_STUCK");
        //delay(CLOCK_DELAY);
        digitalWrite(D4, HIGH);   // CLOCK HIGH
        delayMicroseconds(CLOCK_DELAY);    
        // Set clock back low
        digitalWrite(D4,LOW);     // CLOCK LOW
        delayMicroseconds(CLOCK_DELAY);
        yield();
      }
      digitalWrite(D3,HIGH);     // ENABLE HIGH
      for(int k = 0; k < 8; k++)
      {
        digitalWrite(D4, HIGH);   // CLOCK HIGH
        delayMicroseconds(CLOCK_DELAY);    
        // Set clock back low
        digitalWrite(D4,LOW);     // CLOCK LOW
        delayMicroseconds(CLOCK_DELAY);
        CurrentSensorValue = CurrentSensorValue << 1;
        CurrentSensorValue |= digitalRead(D2);
      }
      digitalWrite(D3,LOW);     // ENABLE LOW

      
      //Serial.print(String(i*8+j));
      //Serial.print(" ");
      //Serial.print(CurrentSensorValue);
      //Serial.println();
      
      sensor_payload += String(CurrentSensorValue);
      sensor_payload += ",";
      //Serial.println();
    }
//    digitalWrite(D1, HIGH);    // ALE goes HIGH
//    delayMicroseconds(CLOCK_DELAY);
//    digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
//    delayMicroseconds(CLOCK_DELAY);
//    digitalWrite(D4, LOW);    // CLOCK GOES LOW
//    delayMicroseconds(CLOCK_DELAY);
//    digitalWrite(D1, LOW);    // ALE goes LOW
//    delayMicroseconds(CLOCK_DELAY);
//    digitalWrite(D4, HIGH);     // CLOCK GOES HIGH
//    delayMicroseconds(CLOCK_DELAY);
//    digitalWrite(D4, LOW);    // CLOCK GOES LOW
//    delayMicroseconds(CLOCK_DELAY);
  }

  // Post that data
  Serial.println(sensor_payload);
  PostSensorValues(sensor_payload);
}


void ConnectWiFi()
{
  WiFi.setOutputPower(0);

  if(WIFI_TYPE == 0)
  {
    WiFi.begin(ssid,password);
    Serial.println("Connecting to Home network");
  }
  else
  {
    WiFi.begin(ssid_UI);
    Serial.println("Connecting to UI network");
  }
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(600);
    Serial.print(".");    
  }
  Serial.println();
  Serial.println(WiFi.localIP());
  delay(1000);
}

void PostSensorValues(String payload)
{
  String url = "http://sensormat.azurewebsites.net/api/SensorImages/PostSensorImageByString";
  Serial.println("Trying to post");
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.addHeader("Content-Length", String(payload.length()));
  http.POST(payload);
  http.writeToStream(&Serial);
  http.end();  
}

void ir1()
{
  sensor_payload += "#";  
}

void ir2()
{
  sensor_payload += "*";  
}
