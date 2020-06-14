# MyAussenlicht
An ESP2866 Based Remote Control for an Aussenlicht 
# Requirements
* Arduino IDE
* WROOM-32 ESP2866 Dev kit
* ESP-Arduino Lib
* ESP Board Files
# Build and Run
Start the Arduino IDE and make sure you have the latest ESP-Lib installed:

![ESP-Lib](Doc/ESP_lib.PNG)

Next, navigate to the baord manager in the Arduino IDE and install the esp8266 library:

![ESP-Lib](Doc/Board_overlay.PNG)

Open the `MyAussenlicht.ino`-file and replace the SSID and password in the following lines with your SSID and password:
```CPP
#ifndef STASSID
#define STASSID "YOUR_SSID"
#define STAPSK  "YOUR_PW"
#endif
```

Choose the `LOLIN(WEMOS) D1 R2 & mini` board, connect your board via USB, select the correct COM-port and press `upload to baord`.

Upon bootup the ESP-module will attempt to connect to the specified WiFi network:

```bash
Connecting to 
YOU_WIFI_NAME
Connecting to WiFi
Sent SSID and PW...
................
WiFi connected
Server started
192.168.178.XX
```