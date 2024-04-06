from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib

HOST = '192.168.207.168'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        #
        content_length = int(self.headers['Content-Length'])
        # Read the posted data
        data = self.rfile.read(content_length).decode()
        # Process the received data (replace with your desired logic)
        print(f"Received data from ESP32: {data}")  

        # Run the external module (replace with your module name)
        try:
            module_name = "sms"  # Replace with your module name
            module = importlib.import_module(module_name).send_sms()
            
            # Call the desired function from the module
           # module.your_function(data)  # Replace with your function name
        except Exception as e:
            print(f"Error running external module: {e}")

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write("Data received and processed successfully!".encode())

with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()