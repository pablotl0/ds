# cliente.py - El servicio español que se conecta al servicio de Los Angeles
import socket
import json
import tkinter as tk
from tkinter import ttk
import threading

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

# Adaptador que convierte distancias de millas a kilómetros
class AdaptadorMillasAKilometros:
    
    def __init__(self, aplicacion_los_angeles):
        self.aplicacion = aplicacion_los_angeles
        self.factor_conversion = 1.60934  # 1 milla = 1.60934 km
    
    # Convierte la distancia en millas a kilómetros        
    def obtener_distancia_km(self, origen, destino):
        distancia_millas = self.aplicacion.obtener_distancia_ruta(origen, destino)
        return distancia_millas * self.factor_conversion

# Interfaz gráfica para el servicio geográfico español
class AplicacionServicioEspanol:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Servicio Geográfico Español")
        self.root.geometry("800x600")
        
        # Creamos el cliente para la aplicación de Los Angeles
        self.cliente_la = ClienteAplicacionLosAngeles()
        
        # Creamos el adaptador
        self.adaptador = AdaptadorMillasAKilometros(self.cliente_la)
        
        # Creamos la interfaz
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        # Configuramos la interfaz de distancias
        self._configurar_interfaz_distancias()
    
    
    # Configura la interfaz de cálculo de distancias
    def _configurar_interfaz_distancias(self):
        # Frame para los controles
        frame_controles = ttk.LabelFrame(self.root, text="Calcular distancia entre ciudades")
        frame_controles.pack(fill=tk.X, padx=10, pady=10)
        
        # Origen
        ttk.Label(frame_controles, text="Ciudad de origen:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.origen_var = tk.StringVar()
        ttk.Entry(frame_controles, textvariable=self.origen_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Destino
        ttk.Label(frame_controles, text="Ciudad de destino:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.destino_var = tk.StringVar()
        ttk.Entry(frame_controles, textvariable=self.destino_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Botón de cálculo
        ttk.Button(frame_controles, text="Calcular Distancia", 
                  command=self._calcular_distancia).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame para mostrar resultados
        frame_resultados = ttk.LabelFrame(self.root, text="Resultados")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto para mostrar resultados
        self.resultado_text = tk.Text(frame_resultados, height=10, width=50, wrap=tk.WORD)
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Ciudades de ejemplo
        frame_ejemplos = ttk.LabelFrame(self.root, text="Ejemplos de ciudades")
        frame_ejemplos.pack(fill=tk.X, padx=10, pady=10)
        
        ciudades = ["Los Angeles", "San Francisco", "San Diego", "Las Vegas", "Madrid", "Barcelona", "Valencia", "Sevilla"]
        for i, ciudad in enumerate(ciudades):
            btn = ttk.Button(frame_ejemplos, text=ciudad, 
                            command=lambda c=ciudad: self._seleccionar_ciudad(c))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky=tk.W)
    
    # Selecciona una ciudad de ejemplo
    def _seleccionar_ciudad(self, ciudad):
        if not self.origen_var.get():
            self.origen_var.set(ciudad)
        else:
            self.destino_var.set(ciudad)
    
    # Calcula la distancia entre dos ciudades        
    def _calcular_distancia(self):
        origen = self.origen_var.get().strip()
        destino = self.destino_var.get().strip()
        
        if not origen or not destino:
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, "Por favor, ingrese origen y destino.")
            return
        
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, f"Calculando distancia entre {origen} y {destino}...\n\n")
        self.root.update()
        
        # Usamos un hilo para no bloquear la interfaz
        def calcular():
            try:
                # Obtenemos la distancia en kilómetros
                distancia_km = self.adaptador.obtener_distancia_km(origen, destino)
                
                # Actualizamos la interfaz
                self.resultado_text.insert(tk.END, f"Distancia: {distancia_km:.2f} kilómetros\n")
                
                # Mostramos también la distancia original en millas para comparación
                distancia_millas = self.cliente_la.obtener_distancia_ruta(origen, destino)
                self.resultado_text.insert(tk.END, f"\nDatos originales del servicio de Los Angeles:\n")
                self.resultado_text.insert(tk.END, f"Distancia: {distancia_millas:.2f} millas\n")
                self.resultado_text.insert(tk.END, f"\nFactor de conversión: 1 milla = 1.60934 km")
                
            except Exception as e:
                self.resultado_text.insert(tk.END, f"Error: {e}")
        
        thread = threading.Thread(target=calcular)
        thread.daemon = True
        thread.start()


# Inicia la aplicación del servicio español
def iniciar_aplicacion():
    root = tk.Tk()
    app = AplicacionServicioEspanol(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()