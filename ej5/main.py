# main.py - Punto de entrada principal para la aplicación
import sys
import threading
import time
from app_espanol import iniciar_aplicacion
import servidor

# Iniciar el servidor en segundo plano
def iniciar_servidor_en_segundo_plano():
    servidor_thread = threading.Thread(target=servidor.start_server)
    servidor_thread.daemon = True  # El hilo se cerrará cuando el programa principal termine
    servidor_thread.start()
    print("Servidor iniciado en segundo plano")
    
    # Esperar un momento para que el servidor se inicie completamente
    time.sleep(1)

# Función principal que inicia tanto el servidor como la aplicación cliente
def main():
    print("Iniciando el sistema de Servicio Geográfico Español...")
    
    # Iniciar el servidor en segundo plano
    iniciar_servidor_en_segundo_plano()
    
    # Iniciar la aplicación cliente
    print("Iniciando la interfaz de usuario...")
    iniciar_aplicacion()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())