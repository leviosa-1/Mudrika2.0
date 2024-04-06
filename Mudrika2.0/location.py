import requests
import xml.etree.ElementTree as ET

# Define the coordinates
coordinates = "22.693159,75.863516"
# Replace 'your_api_key' with your actual API key
api_key = "Enter your geocode.xyz API"

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
    # Print the address components
    print("Street Address:", staddress)
    print("Region:", region)
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code} - {response.text}")
