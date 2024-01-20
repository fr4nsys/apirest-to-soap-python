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

        texto = data["texto"][0]
        telefonos = data["telefonos"][0]

        # Antes de construir la cadena SOAP, reemplaza las variables en el cuerpo SOAP
        soap_body = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:men="edi/Telefonica/Mensaje">
   <soapenv:Header/>
   <soapenv:Body>
      <men:Mensaje>
         <men:Produccion>true</men:Produccion>
         <men:CodAplicacion>FILR</men:CodAplicacion>
         <men:TipoMensaje>1</men:TipoMensaje>
         <men:Texto>{}</men:Texto>
         <men:Telefonos>{}</men:Telefonos>
      </men:Mensaje>
   </soapenv:Body>
</soapenv:Envelope>'''.format(texto, telefonos)

        soap_action = "/Telefonica/Escuchadores/PeticionesEnvio.serviceagent/PeticionesEnvioEndpoint1/RealizaEnvioSMS"

        # Configura la autenticación básica
        username = "tu-usuario"
        password = "tu-contraseña"
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

        # Construye y envía la solicitud SOAP
        response = self.send_soap_request(soap_body, soap_action, credentials)
        self._set_response()
        self.wfile.write(response.encode('utf-8'))

    def send_soap_request(self, soap_body, soap_action, credentials):
        soap_url = "http://tu-servidor-soap.com/tu-endpoint-soap"
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action,
            'Authorization': f'Basic {credentials}'  # Agrega la autenticación básica al encabezado
        }

        # Envía la solicitud SOAP
        response = requests.post(soap_url, headers=headers, data=soap_body)
        return response.text

def run(server_class=HTTPServer, handler_class=S, port=8122):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Iniciando httpd en el puerto {}...".format(port))
    httpd.serve_forever()

if __name__ == "__main__":
    run()
