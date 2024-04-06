from http.server import BaseHTTPRequestHandler, HTTPServer
from twilio.rest import Client
import requests
import xml.etree.ElementTree as ET

HOST = 'IPv4 network'
PORT = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode()
        arr = data.split('#')
        print(f"Received data from ESP32: {arr[1]}, {arr[2]}")
        
        try:
            # Retrieve address information using coordinates
            address = get_address(arr[1], arr[2])
            send_sms(address)
        except Exception as e:
            print(f"Error sending SMS: {e}")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Data received and processed successfully!".encode())

def get_address(latitude, longitude):
    # Define the coordinates
    coordinates = f"{latitude},{longitude}"
    # Replace 'your_api_key' with your actual API key
    api_key = "API key of geocode"
    
    # Define the parameters
    params = {
        "geoit": "xml",
        "auth": api_key
    }
    
    # Define the API endpoint
    url = f"https://geocode.xyz/{coordinates}"
    
    # Make a GET request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        # Extract the <staddress> and <region> elements
        staddress = root.find(".//staddress").text
        region = root.find(".//region").text
        # Construct the address string
        address = f"{staddress}, {region}"
        return address
    else:
        return "Error retrieving address"

def send_sms(data):
    account_sid = "Twillio account_sid"
    auth_token = "Twillio auth_token"
    client = Client(account_sid, auth_token)
    to_number = "receiver's number"
    from_number = "Twillio virtual number "
    message_body = f"Alert! Someone needs your help at Location: {data}"
    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
    print(f"Message sent with SID: {message.sid}")

with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()
