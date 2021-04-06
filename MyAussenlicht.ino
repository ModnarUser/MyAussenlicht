/*@brief: include libary for i2c communication
 https://www.arduino.cc/en/Reference/Wire */
#include <Wire.h>
/*@brief: include librarys for wifi connection
https://www.arduino.cc/en/Reference/WiFi */
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#define SERIAL_BAUD 115200
#define ONBOARD_LED 2
#define D_Pin 15

#ifndef STASSID
#define STASSID "YOUR_SSID"
#define STAPSK "YOUR_PW"
#endif

const char *ssid = STASSID;
const char *password = STAPSK;

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);

String header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
String html_1 = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'/><meta charset='utf-8'><style>body {font-size:140%;} #main {display: table; margin: auto;  padding: 0 10px 0 10px; } h2,{text-align:center; } .button { padding:10px 10px 10px 10px; width:100%;  background-color: #4CAF50; font-size: 120%;}</style><title>LED Control</title></head><body><div id='main'><h2>MyAußenlicht</h2>";
String html_2 = "<form id='F1' action='ON'><input class='button' type='submit' value='ON' ></form><br>";
String html_3 = "<form id='F2' action='OFF'><input class='button' type='submit' value='OFF' ></form><br>";
String html_4 = "</div></body></html>";

String request = "";

void setup()
{
  Serial.begin(SERIAL_BAUD);
  pinMode(D_Pin, OUTPUT);
  pinMode(ONBOARD_LED, OUTPUT);
  Wire.begin();
  delay(1000);
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.persistent(false);

  WiFi.mode(WIFI_STA);
  Serial.print(F("Connecting to WiFi "));
  WiFi.disconnect(true);
  WiFi.begin(ssid, password);
  Serial.print(F("Sent SSID and PW..."));
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(F("."));
  }

  Serial.println();
  Serial.println(F("WiFi connected"));

  // Start the server
  MDNS.begin("aussenlicht");
  server.begin();
  Serial.println(F("Server started"));

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop()
{
  //String send_str = header+html_1+html_2+html_3+html_4
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }

  client.setTimeout(5000);
  while (client.available())
  {
    // byte by byte is not very efficient
    client.read();
  }

  // Read the first line of the request
  request = client.readStringUntil('\r');

  if (request.indexOf("ON") > 0)
  {
    digitalWrite(D_Pin, HIGH);
    digitalWrite(ONBOARD_LED, LOW);
    Serial.println("ON");
  }
  else if (request.indexOf("OFF") > 0)
  {
    digitalWrite(D_Pin, LOW);
    Serial.println("OFF");
    digitalWrite(ONBOARD_LED, HIGH);
  }
  client.print(header);
  client.print(html_1);
  client.print(html_2);
  client.print(html_3);
  client.print(html_4);
  client.flush();

  delay(5);
  // The client will actually be disconnected when the function returns and 'client' object is detroyed
}