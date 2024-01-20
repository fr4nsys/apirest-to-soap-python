# apirest-to-soap-python

# Configuring a REST to SOAP Gateway with Python

In this manual, you will learn how to configure a REST to SOAP Gateway using Python. This gateway will allow you to receive REST requests and convert them into SOAP requests before sending them to a remote SOAP server.

## Prerequisites

- Access to a Linux machine.
- Python 3.x installed on your system.
- Internet access to connect to remote SOAP services.

## Step 1: Configure the Python Script

First, you need to create a Python script that handles REST requests and converts them into SOAP requests. Below is an example of a Python script named `rest_to_soap_gateway.py`.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import urllib.parse
import requests
import base64

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        text = data["text"][0]
        phones = data["phones"][0]

        # Before building the SOAP string, replace variables in the SOAP body
        soap_body = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:men="edi/Telefonica/Mensaje">
   <soapenv:Header/>
   <soapenv:Body>
      <men:Mensaje>
         <men:Producction>true</men:Producction>
         <men:AppCode>CODE</men:AppCode>
         <men:MenType>1</men:MenType>
         <men:Text>{}</men:Text>
         <men:Phones>{}</men:Phones>
      </men:Mensaje>
   </soapenv:Body>
</soapenv:Envelope>'''.format(text, phones)

        soap_action = "/Your/Soap/Action/Endpoint1/ExampleSMS"

        # Set up basic authentication
        username = "your-username"
        password = "your-password"
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

        # Build and send the SOAP request
        response = self.send_soap_request(soap_body, soap_action, credentials)
        self._set_response()
        self.wfile.write(response.encode('utf-8'))

    def send_soap_request(self, soap_body, soap_action, credentials):
        soap_url = "http://your-soap-server.com/your-soap-endpoint"
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action,
            'Authorization': f'Basic {credentials}'  # Add basic authentication to the header
        }

        # Send the SOAP request
        response = requests.post(soap_url, headers=headers, data=soap_body)
        return response.text

def run(server_class=HTTPServer, handler_class=S, port=8122):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd on port {}...".format(port))
    httpd.serve_forever()

if __name__ == "__main__":
    run()
```

Be sure to replace `"your-username"` and `"your-password"` with your actual authentication credentials, and `"http://your-soap-server.com/your-soap-endpoint"` with the actual URL of your SOAP server endpoint.

## Step 2: Run the Script

Save the Python script on your system with the name `rest_to_soap_gateway.py` and run it using Python 3:

```bash
python3 rest_to_soap_gateway.py
```

The server will start and listen on port 8122 for incoming REST requests.

## Step 3: Make REST Requests

Now you can send REST requests to the server on port 8122. Make sure to include the necessary data such as `texto` and `telefonos` in the POST request.

## Step 4: Configured REST to SOAP Gateway

You have successfully configured a REST to SOAP gateway using Python!

## Step 5: Enable the Service at System Startup (Optional)

If you want this service to start automatically when the system boots, you can create a systemd service. Here's an example of how to do it:

1. Create a service file at `/etc/systemd/system/rest_to_soap_gateway.service` with the following content:

```
[Unit]
Description=REST to SOAP Gateway

[Service]
ExecStart=/usr/bin/python3 /path-to-script/rest_to

_soap_gateway.py
Restart=always
User=username
Group=groupname

[Install]
WantedBy=multi-user.target
```

2. Replace `/path-to-script` with the actual location of your `rest_to_soap_gateway.py` script, `username` with the username that will run the service, and `groupname` with the corresponding group name.

3. Enable and start the service:

```bash
sudo systemctl enable rest_to_soap_gateway
sudo systemctl start rest_to_soap_gateway
```

Now, the service will start automatically on system boot.

That's it! You have a configured REST to SOAP gateway ready for use.
