# apirest-to-soap-python

# Configurar un Gateway REST a SOAP con Python

En este manual, aprenderás cómo configurar un Gateway REST a SOAP utilizando Python. Este gateway permitirá recibir solicitudes REST y convertirlas en solicitudes SOAP antes de enviarlas a un servidor SOAP remoto.

***Idioma***
- 🇪🇸 Español
- [🇺🇸 English](https://github.com/fr4nsys/apirest-to-soap-python) 

## Requisitos Previos

- Acceso a una máquina Linux.
- Python 3.x instalado en tu sistema.
- Conexión a Internet para acceder a servicios SOAP remotos.

## Paso 1: Configurar el Script Python

Primero, necesitas crear un script Python que maneje las solicitudes REST y las convierta en solicitudes SOAP. A continuación, tienes un ejemplo de un script de Python llamado `rest_to_soap_gateway.py`.

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
```

Asegúrate de reemplazar `"tu-usuario"` y `"tu-contraseña"` con tus propias credenciales de autenticación, y `"http://tu-servidor-soap.com/tu-endpoint-soap"` con la URL real de tu punto de conexión SOAP.

## Paso 2: Ejecutar el Script

Guarda el script Python en tu sistema con el nombre `rest_to_soap_gateway.py` y ejecútalo usando Python 3:

```bash
python3 rest_to_soap_gateway.py
```

El servidor se ejecutará y escuchará en el puerto 8122 para las solicitudes REST entrantes.

## Paso 3: Realizar Solicitudes REST

Ahora puedes enviar solicitudes REST al servidor en el puerto 8122. Asegúrate de incluir los datos necesarios, como `texto` y `telefonos`, en la solicitud POST.

## Paso 4: Gateway REST a SOAP Configurado

¡Has configurado con éxito un gateway REST a SOAP utilizando Python!

## Paso 5: Habilitar el Servicio al Inicio del Sistema (Opcional)

Si deseas que este servicio se inicie automáticamente al arrancar el sistema, puedes crear un servicio systemd. Aquí tienes un ejemplo de cómo hacerlo:

1. Crea un archivo de servicio en `/etc/systemd/system/rest_to_soap_gateway.service` con el siguiente contenido:

```
[Unit]
Description=Gateway REST a SOAP

[Service]
ExecStart=/usr/bin/python3 /ruta-al-script/rest_to_soap_gateway.py
Restart=always
User=nombre-de-usuario
Group=nombre-de-grupo

[Install]
WantedBy=multi-user.target
```

2. Reemplaza `/ruta-al-script` con la ubicación real de tu script `rest_to_soap_gateway.py`, `nombre-de-usuario` con el nombre de usuario que ejecutará el servicio y `nombre-de-grupo` con el nombre del grupo correspondiente.

3. Habilita y comienza el servicio:

```bash
sudo systemctl enable rest_to_soap_gateway
sudo systemctl start rest_to_soap_gateway
```

Ahora, el servicio se iniciará automáticamente al arrancar el sistema.

¡Eso es todo! Ahora tienes un gateway REST a SOAP configurado y listo para usar.
