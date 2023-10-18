import time
import requests
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import smtplib

# Server URLs
server_url_1 = 'http://1.example.com/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DataCollection=3PInverterData&DeviceId=1' #Fronius Inverter API
server_url_2 = 'http://1.example.com/solar_api/v1/GetMeterRealtimeData.cgi' #Fronius Smart Meter API
server_url_3 = 'http://2.example.com'#CT-Microcontroller 1 
server_url_4 = 'http://3.example.com'#CT-Microcontroller 2

# InfluxDB configuration
url = 'http://influx.example.com'
token = 'exampletoken'
org = 'exampleorg'
bucket = 'examplebucket'
influx_measurement = 'power_data'

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Error count and threshold
error_count = 0
error_threshold = 4  # Adjust this threshold as needed

# Email configuration
email_sender = 'sender@example.com'  # Replace with your configured email sender address
email_recipient = 'recipient@exampl.com'  # Replace with the recipient's email address
email_subject = 'Error in Script'
email_password = 'exampleGMailAppPassword'

def send_email(subject, message):
    try:
        # Connect to the local Postfix server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Use 'gmail' as the SMTP server
        msg = f"Subject: {subject}\n\n{message}"  # Include the subject and message
        server.login(email_sender, email_password)        
        server.sendmail(email_sender, [email_recipient], msg)
        server.quit()
        print("Notification email sent successfully.")
    except Exception as e:
        print("Error sending email:", str(e))

try:
    while True:
        try:
            # Send HTTP requests to the servers
            response_1 = requests.get(server_url_1)
            data_1 = response_1.json()
            response_2 = requests.get(server_url_2)
            data_2 = response_2.json()
            response_3 = requests.get(server_url_3, timeout=5)  # Add a timeout to the request
            data_3 = response_3.json()
            response_4 = requests.get(server_url_4, timeout=5)  # Add a timeout to the request
            data_4 = response_4.json()
             
            
            # Take the absolute value of power factor before storing in InfluxDB Point
            abs_power_factor_1 = abs(data_2['Body']['Data']['0']['PowerFactor_Phase_1'])
            abs_power_factor_2 = abs(data_2['Body']['Data']['0']['PowerFactor_Phase_2'])
            abs_power_factor_3 = abs(data_2['Body']['Data']['0']['PowerFactor_Phase_3'])

            point = Point("power_data") \
                .time(data_1['Head']['Timestamp']) \
                .field("PowerFactor_Phase_1", abs_power_factor_1) \
                .field("PowerFactor_Phase_2", abs_power_factor_2) \
                .field("PowerFactor_Phase_3", abs_power_factor_3) \
                .field("Voltage_AC_Phase_1_Zaehler", data_2['Body']['Data']['0']['Voltage_AC_Phase_1']) \
                .field("Voltage_AC_Phase_2_Zaehler", data_2['Body']['Data']['0']['Voltage_AC_Phase_2']) \
                .field("Voltage_AC_Phase_3_Zaehler", data_2['Body']['Data']['0']['Voltage_AC_Phase_3']) \
                .field("Current_AC_Phase_1_Zaehler", data_2['Body']['Data']['0']['Current_AC_Phase_1']) \
                .field("Current_AC_Phase_2_Zaehler", data_2['Body']['Data']['0']['Current_AC_Phase_2']) \
                .field("Current_AC_Phase_3_Zaehler", data_2['Body']['Data']['0']['Current_AC_Phase_3']) \
                .field("Current_AC_Phase_1_Wechselrichter", data_1['Body']['Data']['IAC_L1']['Value']) \
                .field("Current_AC_Phase_2_Wechselrichter", data_1['Body']['Data']['IAC_L2']['Value']) \
                .field("Current_AC_Phase_3_Wechselrichter", data_1['Body']['Data']['IAC_L3']['Value']) \
                .field("ct_0_value", data_3 ['ct_0']) \
                .field("ct_1_value", data_3 ['ct_1']) \
                .field("ct_2_value", data_3 ['ct_2']) \
                .field("ct_3_value", data_3 ['ct_3']) \
                .field("ct_4_value", data_4 ['ct_0']) \
                .field("ct_5_value", data_4 ['ct_1']) \
                .field("ct_6_value", data_4 ['ct_2']) \
                .field("ct_7_value", data_4 ['ct_3']) \
                .field("ct_8_value", data_4 ['ct_4'])
                
            # Write data to InfluxDB
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=point)
            print("Data written to InfluxDB successfully.")
            error_count = 0

        except requests.RequestException as req_ex:
            error_count += 1
            error_message = f"Error in HTTP request: {req_ex}"
            print(error_message)
            if error_count == error_threshold or error_count%360 == 0:
                send_email(email_subject, error_message)
                time.sleep(10)  # Wait before retrying
            else:
                time.sleep(10)

except KeyboardInterrupt:
    print("Script terminated by user.")

finally:
    # Close the InfluxDB connection
    client.close()
