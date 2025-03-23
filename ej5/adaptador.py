# adaptador.py - Adaptador que convierte distancias de millas a kilómetros
from servicio_geografico import ServicioGeografico
from cliente_la import ClienteAplicacionLosAngeles

class AdaptadorMillasAKilometros(ServicioGeografico):
    
    def __init__(self, aplicacion_los_angeles=None):
        # Si no se proporciona una instancia, creamos una nueva
        if aplicacion_los_angeles is None:
            self.aplicacion = ClienteAplicacionLosAngeles()
        else:
            self.aplicacion = aplicacion_los_angeles
            
        self.factor_conversion = 1.60934  # 1 milla = 1.60934 km
    
    # Implementa la interfaz del ServicioGeografico        
    def calcular_distancia(self, origen, destino):
        distancia_millas = self.aplicacion.obtener_distancia_ruta(origen, destino)
        return distancia_millas * self.factor_conversion