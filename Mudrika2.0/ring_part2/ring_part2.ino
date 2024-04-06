#include <WiFi.h>
#include <TinyGPSPlus.h>
#include <ESP32Servo.h>

//Define LED and button pins
const char* ssid = "Wifi network SSID";
const char* password = "Wifi Password";
const char* server_address = "Wifi IPv4 Address"; // Replace with your laptop's IP address
const int port = 8080; // Replace with the port used by your Python script
const int buttonPin = 13;
const int servoPin =12;
const int servo_led1=27;
const int servo_led2=26;
const int green_led=25;
const int buzzerPin=14;
const int rxPin = 16;
const int txPin = 17;
const uint32_t baudRate = 9600;
int servoPos=45;
// GPS and software serial objects
WiFiClient client;
TinyGPSPlus gps;
Servo myservo;
//function for coordinates
double* get_coord() {
  // Read data from Serial2 and feed it to TinyGPS++
  while (Serial2.available()) {
    gps.encode(Serial2.read());
  }

  // Check if GPGGA sentence is updated
  if (gps.location.isUpdated()) {
    // Extract latitude and longitude
    double* coord = new double[2];
    coord[0] = gps.location.lat(); // latitude
    coord[1] = gps.location.lng(); // longitude
    

    // Print or store the values as needed
    // Serial.print("Latitude: ");
    // Serial.println(coord[0], 6);
    // Serial.print("Longitude: ");
    // Serial.println(coord[1], 6);
    return coord;
  }else{
    return nullptr;
  }
}


void setup() {
  Serial.begin(115200);
 WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
   Serial2.begin(baudRate, SERIAL_8N1, rxPin, txPin);  // Use Serial2 for GPS
 
  // Set LED pin as output
  // Set Buzzer pin as output
  myservo.attach(servoPin);
  pinMode(servo_led1,OUTPUT);
  pinMode(servo_led2,OUTPUT); 
  pinMode(buzzerPin,OUTPUT);
  pinMode(green_led, OUTPUT);
 // Set button pin as input with pull-up resistor
  pinMode(buttonPin, INPUT_PULLUP);
}
unsigned long current_time;
unsigned long start_time;
int count=0;
void loop() {
double* coord;
int button=digitalRead(buttonPin);
if(button==LOW){
  count++;
  if(count==1){
    start_time=millis();
    current_time=start_time;
    
  }
  if(count==2||count==3){
    current_time=millis();
  }
  delay(200);
}
//Serial.println(current_time-start_time);
if((1<=count<=3)&&(current_time-start_time>=10000)){
count=0;
}
if (count>=3){
  coord= get_coord();
  send_coord(coord);
  alarm_police();
  client_call(coord);
  delete[] coord;
}
}
void reconnect() {
  while (!client.connect(server_address, port)) {
    Serial.println("Connecting to server...");
    delay(5000);
  }
  Serial.println("Connected to server");
}

void send_coord(double *coord){
  count = 0;
  digitalWrite(green_led, HIGH);
  delay(300);
  digitalWrite(green_led,LOW);
  // Print the current position to the serial monitor
  // Print or store the values as needed
     if (coord != nullptr){
       Serial.print("Latitude: ");
       Serial.println(coord[0], 6);
       Serial.print("Longitude: ");
       Serial.println(coord[1], 6);
      //  delete[] coord;
    }
  // Delay for 1 second
  delay(10);
  //alarm_police();

}
void alarm_police(){
  delay(1000);
 for(int i=0;i<10;i++){
  digitalWrite(servo_led1,HIGH);
  digitalWrite(servo_led2,LOW);
  digitalWrite(buzzerPin,HIGH);
  myservo.write(90);
  delay(250);
  digitalWrite(servo_led1,LOW);
  digitalWrite(servo_led2,HIGH);
  myservo.write(0);
  delay(250);}
  digitalWrite(servo_led1,LOW);
  digitalWrite(servo_led2,LOW);
  digitalWrite(buzzerPin,LOW);
}
void client_call(double* coord){
  count=0;
    if (!client.connected()) {
    reconnect();
  }

   // Send data to the server (coordinates only)
  client.print("POST /data HTTP/1.1\r\n");
  client.print("Host: ");
  client.print(server_address);
  client.print("\r\n");
  client.print("Content-Length: ");
  // Calculate the length of the data
    // Serial.println(coord[0]);

  String data ="#"+ String(coord[0],6) + "#" + String(coord[1],6);
  client.print(data.length()+74);
  client.println("\r\n");
  client.println("Content-Type: text/plain");
  client.println("\r\n");
  // Send the coordinates
  Serial.println(data);
  client.println(data);

  client.stop();
  delay(1000);
}
