                                                                                       

#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
 
const char* ssid = "Supernet_WiFi_33FC";
const char* password = "67AQM7QJMY7";

int ON_LED = 14;
int OKAY_LED =16;
int IN_SWITCH =15;
int ERROR_LED = 33;
String inout;
StaticJsonDocument<200> doc;
LiquidCrystal_I2C lcd(0x27, 16, 2);
//#define RST_PIN 9 // Configurable, see typical pin layout above
//#define SS_PIN 10 // Configurable, see typical pin layout above
const int RST_PIN = 22; // Reset pin
const int SS_PIN = 5; // Slave select pin
byte readCard[4];   
 
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
 
void setup() {
  lcd.begin();

  // Turn on the blacklight and print a message.
  lcd.backlight();
  lcd.print("Welcome to CPMS!");
  lcd.setCursor(0,1);
  lcd.print("Booting...");
  pinMode (ON_LED, OUTPUT);
  pinMode (OKAY_LED, OUTPUT);
  pinMode (ERROR_LED, OUTPUT);
  pinMode (IN_SWITCH, INPUT_PULLDOWN);
  pinMode(12,OUTPUT);
  digitalWrite(12,HIGH);
  if (digitalRead(IN_SWITCH)==LOW){
     inout = "in";
  }
  else{
     inout = "out";
  }
Serial.begin(9600);
  delay(2000);   
 lcd.clear();
 lcd.print(inout);lcd.print(" mode.");
 
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(500);}
lcd.clear();
      lcd.setCursor(0,1);
      lcd.print("IP: ");
      lcd.print(WiFi.localIP());
//Serial.begin(9600); // Initialize serial communications with the PC
//while (!Serial); // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
SPI.begin(); // Init SPI bus
mfrc522.PCD_Init(); // Init MFRC522
//mfrc522.PCD_DumpVersionToSerial(); // Show details of PCD - MFRC522 Card Reader details
Serial.println("The Sensor is in ");
Serial.print(inout);
Serial.print(" mode");
digitalWrite(ON_LED,HIGH);
digitalWrite(OKAY_LED,HIGH);

}
 
void loop() {
if ( ! mfrc522.PICC_IsNewCardPresent())  // If statement that looks for new cards.
  {
    return;
  }

  if ( ! mfrc522.PICC_ReadCardSerial())    // If statement that selects one of the cards.
  {
    return;
  }
  String content= "";
  byte letter;
  Serial.print("UID: ");    
  for (int i = 0; i < mfrc522.uid.size; i++) {  
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));        // Prints RFID cards UID to the serial monitor.
  }
  Serial.println(content);
  Serial.println(sizeof(content));

  mfrc522.PICC_HaltA();
  digitalWrite(OKAY_LED,HIGH);
  lcd.clear();
  lcd.print("processing");
  HTTPClient http;   
 
   http.begin("https://carparkingsystem.herokuapp.com/getdata/");  //Specify destination for HTTP request
   http.addHeader("Content-Type",  "application/x-www-form-urlencoded");//Specify content-type header

   String temp1 = "rfid=";
   //String temp2 = "&inout=";
   //String temp3 = "&pwd=lolhaha";
   content.remove(0,1);
   String tmpstr = temp1 + content;
   tmpstr += "&inout=";
   tmpstr += inout;
   tmpstr += "&pwd=lolhaha&parking=PyinOoLwin";
  
   Serial.println(tmpstr);
   int httpResponseCode = http.POST(tmpstr);//Send the actual POST request
   digitalWrite(OKAY_LED,LOW);
 
   if(httpResponseCode==200){
    lcd.clear();
    String payload = http.getString();
    Serial.println(payload);
    deserializeJson(doc, payload);
    String car_number =doc["car_number"];
    int balance = doc["balance"];
    lcd.print(car_number);
    lcd.setCursor(0,1);
    lcd.print(balance);
    
    if(balance <= 0){
      delay(1500);
      lcd.clear();
      lcd.print("Balance is low.");
      lcd.setCursor(0,1);
      lcd.print("Please top up");
      
    }

  //Print return code
 delay(5000);
   }else{
 digitalWrite(ERROR_LED,HIGH);
 lcd.clear();
    lcd.print("Error: ");
    lcd.print(httpResponseCode);
    delay(5000);
    digitalWrite(ERROR_LED,LOW);
 
   }  //Free resources
 http.end();
 lcd.clear();
 lcd.print("Welcome to CPMS");
 }   
