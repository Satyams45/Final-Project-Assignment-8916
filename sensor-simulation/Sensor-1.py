import time
import json
from datetime import datetime
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=Satyam8916.azure-devices.net;DeviceId=Sensor-1;SharedAccessKey=GbUitUSvYU8fOqyV2ihKMAVIaIJDztrzfzD+NK2FnUA="

LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]

def generate_data(location):
    return {
        "location": location,
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": random.randint(-10, 2),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": random.randint(-15, 5),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print("Simulating sensors... Press Ctrl+C to stop.")

    while True:
        for location in LOCATIONS:
            payload = generate_data(location)
            message = Message(json.dumps(payload))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            client.send_message(message)
            print(f"Sent message: {payload}")
        time.sleep(10)

if __name__ == "__main__":
    main()
