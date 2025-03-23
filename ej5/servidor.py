# servidor.py - Simula la aplicación de Los Angeles (servicio remoto)
import socket
import json
import threading
import hashlib

# Aplicación de navegación de Los Angeles que trabaja con millas
class AplicacionLosAngeles:
    
    # Simulamos una distancia basada en los nombres de las ciudades
    def obtener_distancia_ruta(self, origen, destino): 
        # Generamos un número basado en los nombres para que sea consistente
        hash_value = int(hashlib.md5(f"{origen}-{destino}".encode()).hexdigest(), 16)
        return (hash_value % 500) + 50  # Entre 50 y 550 millas
    
# Maneja la conexión con un cliente    
def handle_client(client_socket):
    app = AplicacionLosAngeles()
    
    try:
        # Recibimos datos del cliente
        request_data = client_socket.recv(4096).decode('utf-8')
        request = json.loads(request_data)
        
        # Procesamos la solicitud
        if request["metodo"] == "obtener_distancia":
            origen = request["origen"]
            destino = request["destino"]
            distancia = app.obtener_distancia_ruta(origen, destino)
            response = {"distancia": distancia}
        
        else:
            response = {"error": "Método no reconocido"}
        
        # Enviamos la respuesta
        client_socket.send(json.dumps(response).encode('utf-8'))
    
    except Exception as e:
        print(f"Error al manejar cliente: {e}")
    
    finally:
        client_socket.close()

def start_server():

    # Inicia el servidor de la aplicación de Los Angeles
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9000))
    server.listen(5)
    print("Servidor de la Aplicación de Los Angeles iniciado en localhost:9000")
    
    try:
        while True:
            client_sock, address = server.accept()
            print(f"Conexión aceptada de {address[0]}:{address[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_sock,))
            client_handler.start()
    
    except KeyboardInterrupt:
        print("Servidor detenido.")
    
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
