"Automatic Car Parking Management System"

The Automatic Car Parking Management System is composed of two main subsystems. There is a web server system and a client system. At the client side, ESP32 is used to perform control functions and RC522 is used for detecting cars through a counter system. The metadata of cars passing through is delivered to the central web server. The server stores the numbers of cars going in and out of each parking. It also calculates the cost of parking for each vehicle depending on the length of its parking time.

The car drivers can also check whether a parking has a vacant space or not through a website, which is also hosted by the web server. A web application is chosen because it can work in almost every popular mobile platform. Car owners can also keep track of parking data of their cars and parking costs.

When a car gets to the entrance of the car parking, the RFID card licensed to the car will be requested. The driver has to place the card near the sensor. The sensor will scan for the first eight words on the RFID card and send them to the ESP32. The ESP32 take these words and turn them into a http POST data stream together with the car parking name, whether the sensor is at in or out mode and the API key. The http POST stream is then sent to the web server through the internet using ESP32’s Wi-Fi capabilities.

The web server processes the received data. First, it checks whether the API key is right or wrong. Then, it checks whether the RFID card keywords are registered or not. If something turns negative, the web server sent respective error codes back to the ESP32 to show error codes on the LCD Display.

If everything is normal, the server sends code 200 back and saves the respective car number into the database of respective car parking together with the exact time the car enters or leave. If the car is going out, the out flag is triggered and the cost of parking is calculated and subtracted from the billing database.
