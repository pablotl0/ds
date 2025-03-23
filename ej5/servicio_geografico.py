# servicio_geografico.py - Interfaz para servicios geográficos
from abc import ABC, abstractmethod

class ServicioGeografico(ABC):
    @abstractmethod
    def calcular_distancia(self, origen, destino):
        """Calcula la distancia entre dos ubicaciones en kilómetros"""
        pass