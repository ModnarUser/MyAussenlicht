# MyAussenlicht
MyAussenlicht is an ESP2866 based remote control for an outdoor light. A simple server running on the ESP2866, that can be accessed via your local network, is utilized. Two use cases are supported:
* Manual Remote Control
* Automated Remote Control with Sunrise and Sunset 
## Requirements
* Arduino IDE
* WROOM-32 ESP2866 Dev kit
* ESP-Arduino Lib
* ESP Board Files
## Build and Run
Start the Arduino IDE and make sure you have the latest ESP-Lib installed:

![ESP-Lib](Doc/ESP_lib.PNG)

Next, navigate to the board manager in the Arduino IDE and install the esp8266 library:

![ESP-Lib](Doc/Board_overlay.PNG)

Open the `MyAussenlicht.ino`-file and replace the SSID and password in the following lines with your SSID and password:
```CPP
#ifndef STASSID
#define STASSID "YOUR_SSID"
#define STAPSK  "YOUR_PW"
#endif
```

Choose the `LOLIN(WEMOS) D1 R2 & mini` board, connect your board via USB, select the correct COM-port and press `upload to board`.

Upon bootup the ESP-module will attempt to connect to the specified WiFi network:

```bash
Connecting to 
YOUR_WIFI_NAME
Connecting to WiFi
Sent SSID and PW...
................
WiFi connected
Server started
192.168.178.XX
```
## Manual Remote Control
Grab a device already connected to your local network and access the IP address from above (`192.168.178.XX`).

![Landing Page For Remote Control](Doc/LandingPage.PNG)

Now you can toggle the Aussenlicht by simply pressing the `ON` or `OFF` button.

## Automated Remote Control
### Requirements
* Machine that is permanently connected to your local Network (e.g. Raspberry Pi, NAS, etc.)
* At least Python 3.6
* cron
### Example Setup using a QNAP2
### Testing
Install all python requirements via

```Powershell
pip install -r requirements.txt
```

Modify the `TEST_URL` in `test_MyAussenlichtTimer.py` to fit your server URL.
```Python
################################################################
# Test Settings
################################################################

TEST_URL = "http://192.168.178.XX"  # Use URL of your Aussenlicht

```
Navigate into the toplevel directory (`*/MyAussenlicht`) and run the tests.

```Powershell
pytest test_MyAussenlichtTimer.py
```
When all tests were run successfully you should get the following output:

```Powershell
PS D:\MyAussenlicht> pytest .\test_MyAussenlichtTimer.py
================================================================= test session starts ==================================================================
platform win32 -- Python 3.7.9, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: D:\MyAussenlicht
collected 4 items

test_MyAussenlichtTimer.py ....                                                                                                                   [100%] 

======================================================= 4 passed in 68.29s (0:01:08) ======================================================== 
```
