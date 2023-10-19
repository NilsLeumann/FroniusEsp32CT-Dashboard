import random
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB configuration
url = 'example.com:8086'
token = 'exampletoken'
org = 'exampleorg'
bucket = 'examplebucket'

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Create a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Generate and send random numbers every second
while True:
    # Generate a random number
    random_number = random.uniform(0, 100)

    # Create an InfluxDB point
    point = Point('random_measurement') \
        .tag('source', 'python_script') \
        .field('value', random_number) \
        .time(datetime.utcnow())

    # Write the point to the database
    write_api.write(bucket=bucket, org=org, record=point)

    print(f"Sent random number: {random_number}")

    # Wait for one second before sending the next number
    time.sleep(1)