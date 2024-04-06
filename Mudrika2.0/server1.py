from http.server import BaseHTTPRequestHandler, HTTPServer
from twilio.rest import Client
import importlib
HOST = '192.168.1.17'
PORT = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode()
        arr= data.split('#')
        print(f"Received data from ESP32: {arr[1],arr[2]}") 
        
        try:
            send_sms(arr[1]+','+arr[2])
        except Exception as e:
            print(f"Error sending SMS: {e}")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Data received and processed successfully!".encode())

def send_sms(data):
    account_sid = "AC091ddcdbd3f3a86db5c7ab71145435fe"
    auth_token = "6c9750c149dbe1580668098e140f319a"
    client = Client(account_sid, auth_token)
    to_number = "+917024896018"
    from_number = "+16592518494"
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
