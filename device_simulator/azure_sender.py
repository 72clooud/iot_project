import os
import json
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

load_dotenv()

class AzureIotHubSender:
    def __init__(self):
        self.iot_device_key = os.getenv('AZURE_IOT_CONNECTION_STRING')
        try:
            self.client = IoTHubDeviceClient.create_from_connection_string(self.iot_device_key)
        except Exception as e:
            raise ConnectionError(f"You can not create client for IoT Hub {e}")
        
    def connect(self):
        try:
            self.client.connect()
        except Exception as e:
            print(f'Connection error: {e}')
    
    def disconnect(self):
        try:
            self.client.disconnect()
        except Exception as e:
            print(f'Disconnect error: {e}')

    def send_telemetry_message(self, data_dict: dict) -> bool:
        data_json = json.dumps(data_dict)
        message = Message(data=data_json, content_type="application/json")
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        try:
            self.client.send_message(message)
            print("Message successfully sent")
            return True
        except Exception as e:
            print(f'Error while sending a message - error: {e}')
            return False
        