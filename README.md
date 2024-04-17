# Readme

## Microcontroller Setup:

1. Connect the microcontroller for the sensors via USB to a PC.

2. Upload, configure and execute the following script using Arduino IDE:
   - Script Link: [ArduinoCode.ino](https://github.com/NilsLeumann/FroniusEsp32CT-Dashboard/blob/main/ArduinoCode.ino)

## Server Setup:

1. Set up a fresh installation of Ubuntu 22.04 with root user privileges. Install all required software. You can follow these steps:

   - Update the package list and upgrade installed packages:
     ```
     apt update && apt -y upgrade
     ```

   - Install required packages:
     ```
     apt install -y pip curl net-tools
     ```

   - Install InfluxDB by following this tutorial: [InfluxDB Installation Guide](https://docs.influxdata.com/influxdb/v2/install/?t=Linux)

   - Install Grafana by following this tutorial: [Grafana Installation Guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/)

   - Reload the systemd manager configuration:
     ```
     systemctl daemon-reload
     ```

   - Enable the Grafana server to start on boot:
     ```
     systemctl enable grafana-server
     ```

   - Install the InfluxDB Python client:
     ```
     pip install influxdb-client
     ```

2. Obtain the server's IP address using the following command:
   ```
   ifconfig
   ```

3. Access the following URLs in your web browser:
   - Grafana: [http://your-ip:3000](http://your-ip:3000)
   - InfluxDB: [http://your-ip:8086](http://your-ip:8086)

4. In InfluxDB, create an account and a database.

5. Download the Python script to your server:
   ```
   wget https://github.com/NilsLeumann/FroniusEsp32CT-Dashboard/blob/main/PythonCode.py
   ```

6. Download the Grafana dashboard from GitHub onto your PC:
   https://github.com/NilsLeumann/FroniusEsp32CT-Dashboard/blob/main/Grafana-Dashboard.json

7. Import the downloaded dashboard in Grafana and customize names and graphs as needed and add InfluxDB as a Datasource.

8. Customize the Python code file:
   ```
   nano PythonCode.py
   ```

9. Run the Python script:
   ```
   python3 PythonCode.py
   ```

Your system should now be set up and ready to use with the microcontroller and the server.
