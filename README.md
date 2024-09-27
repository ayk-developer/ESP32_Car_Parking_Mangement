## Automatic Car Parking Management System

### Motivation

Inspired by the need for a more efficient way to manage car parking, this project aims to automate the process using modern technology. By leveraging an ESP32 microcontroller and a web server, we can provide real-time parking information, calculate fees accurately, and track vehicle records seamlessly.

### How it Works

1. **Car Detection:**
   - The RC522 RFID reader at the parking entrance detects incoming vehicles.
2. **RFID Card Scanning:**
   - The driver presents their RFID card to the sensor.
3. **Data Transmission:**
   - The ESP32 microcontroller reads the RFID card data and sends it to the web server.
4. **Server Processing:**
   - The web server validates the RFID card and updates the parking database.
   - For exiting cars, it calculates the parking fee based on duration.
5. **Response:**
   - The server sends a response to the ESP32, indicating success or failure.

### Features

* **Real-time parking availability:** Users can check available parking spaces through a web interface.
* **Fee calculation:** The system automatically calculates parking fees based on duration.
* **Vehicle tracking:** Car owners can view their parking history and costs.
* **RFID card authentication:** Ensures secure access to the parking.
* **Error handling:** Provides informative messages for invalid inputs or system errors.

### Technologies

* **ESP32:** Microcontroller for client-side control.
* **RC522:** RFID reader for card detection.
* **Web server:** Handles data processing and provides a user interface.
* **HTTP:** Communication protocol between client and server.
* **Database:** Stores parking data and billing information.

### Future Enhancements

* **Payment integration:** Allow users to pay parking fees directly through the web interface.
* **Mobile app:** Develop a mobile app for easier access and user experience.
* **Notifications:** Send notifications to users when their parking time is nearing expiration.
* **Integration with other systems:** Connect the system to traffic management or security systems.

### License

This project is distributed under the MIT License
