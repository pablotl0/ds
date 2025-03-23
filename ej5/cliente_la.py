# cliente_la.py - Cliente para la aplicación de Los Angeles
import socket
import json

# Cliente para la aplicación de Los Angeles
class ClienteAplicacionLosAngeles:
    
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
    
    # Envía una solicitud al servidor y recibe la respuesta
    def _enviar_solicitud(self, solicitud):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((self.host, self.port))
            client.send(json.dumps(solicitud).encode('utf-8'))
            response_data = client.recv(4096).decode('utf-8')
            return json.loads(response_data)
        
        finally:
            client.close()
    
    # Obtiene la distancia entre dos ciudades
    def obtener_distancia_ruta(self, origen, destino):
        solicitud = {
            "metodo": "obtener_distancia",
            "origen": origen,
            "destino": destino
        }
        
        respuesta = self._enviar_solicitud(solicitud)
        return respuesta.get("distancia")