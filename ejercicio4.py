from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

# Interfaz para los filtros
class Filter(ABC):
    """Interfaz abstracta para los filtros de intercepción."""
    
    @abstractmethod
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        """
        Ejecuta el filtro sobre la solicitud.
        
        Args:
            request: Diccionario con los datos de la solicitud
            
        Returns:
            Mensaje de error si la validación falla, None si pasa
        """
        pass

# Filtro para validar el formato de correo electrónico
class EmailFormatFilter(Filter):
    """Filtro que valida que el correo contenga texto antes del @."""
    
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        email = request.get('email', '')
        
        if '@' not in email:
            return "El correo debe contener el carácter @"
        
        username = email.split('@')[0]
        if not username:
            return "El correo debe contener texto antes del carácter @"
        
        return None

# Filtro para validar el dominio del correo electrónico
class EmailDomainFilter(Filter):
    """Filtro que valida que el dominio del correo sea gmail.com o hotmail.com."""
    
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        email = request.get('email', '')
        
        if '@' not in email:
            return "El correo debe contener el carácter @"
        
        domain = email.split('@')[1].lower()
        allowed_domains = ['gmail.com', 'hotmail.com']
        
        if domain not in allowed_domains:
            return f"El dominio del correo debe ser uno de los siguientes: {', '.join(allowed_domains)}"
        
        return None

# Filtro para validar la longitud de la contraseña
class PasswordLengthFilter(Filter):
    """Filtro que valida que la contraseña tenga al menos 8 caracteres."""
    
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        password = request.get('password', '')
        
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres"
        
        return None

# Filtro para validar que la contraseña contenga al menos un número
class PasswordNumberFilter(Filter):
    """Filtro que valida que la contraseña contenga al menos un número."""
    
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        password = request.get('password', '')
        
        if not any(char.isdigit() for char in password):
            return "La contraseña debe contener al menos un número"
        
        return None

# Filtro para validar que la contraseña contenga al menos un carácter especial
class PasswordSpecialCharFilter(Filter):
    """Filtro que valida que la contraseña contenga al menos un carácter especial."""
    
    def execute(self, request: Dict[str, Any]) -> Optional[str]:
        password = request.get('password', '')
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        
        if not any(char in special_chars for char in password):
            return "La contraseña debe contener al menos un carácter especial"
        
        return None

# Clase que mantiene la cadena de filtros
class FilterChain:
    """Cadena de filtros que procesa secuencialmente una solicitud."""
    
    def __init__(self):
        """Inicializa una cadena de filtros vacía."""
        self.filters: List[Filter] = []
        self.target = None
        
    
    def add_filter(self, filter_obj: Filter) -> 'FilterChain':
        """
        Añade un filtro a la cadena.
        
        Args:
            filter_obj: El filtro a añadir
            
        Returns:
            La instancia de FilterChain para permitir encadenamiento
        """
        self.filters.append(filter_obj)
        return self
    
    def set_target(self, target):
        """
        Establece el objetivo al que se enviará la solicitud si pasa todos los filtros.
        
        Args:
            target: El objeto destino que procesará la solicitud
        """
        self.target = target

    def execute(self, request: Dict[str, Any]) -> List[str]:
        """
        Ejecuta todos los filtros en la cadena sobre la solicitud.
        
        Args:
            request: Diccionario con los datos de la solicitud
            
        Returns:
            Lista de mensajes de error, vacía si todos los filtros pasan
        """
        errors = []
        
        for filter_obj in self.filters:
            error = filter_obj.execute(request)
            if error:
                errors.append(error)
        
        return errors

# Clase que gestiona la solicitud y aplica los filtros
class FilterManager:
    """Gestor de filtros que aplica la cadena de filtros a una solicitud."""
    
    def __init__(self, target):
        """
        Inicializa el gestor con un objetivo.
        
        Args:
            target: El objeto destino que procesará la solicitud si pasa todos los filtros
        """
        self.filter_chain = FilterChain()
        self.filter_chain.set_target(target)
    
    def add_filter(self, filter : Filter):
        """
        Añade un filtro a la cadena de filtros.
        
        Args:
            filter: Filtro a añadir a la cadena
        """
        self.filter_chain.add_filter(filter)
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una solicitud aplicando los filtros y enviándola al destino si pasa.
        
        Args:
            request: Diccionario con los datos de la solicitud
            
        Returns:
            Diccionario con el resultado del procesamiento
        """
        errors = self.filter_chain.execute(request)
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Si pasa todos los filtros, envía al destino
        return self.target.process(request)

# Clase objetivo que procesa la solicitud (existente, no se debe modificar)
class AuthenticationService:
    """Servicio de autenticación que procesa las credenciales."""
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una solicitud de autenticación.
        
        Args:
            request: Diccionario con los datos de la solicitud
            
        Returns:
            Diccionario con el resultado del procesamiento
        """

        return {
            'success': True,
            'message': f"Autenticación exitosa para el usuario {request.get('email')}"
        }

# Cliente que utiliza el sistema
def main():
    """Función principal que ejecuta el programa."""
    # Crear el servicio de autenticación (clase existente)
    auth_service = AuthenticationService()
    
    # Crear el gestor de filtros
    filter_manager = FilterManager(auth_service)
    
    # Añadir filtros para el correo
    filter_manager.add_filter(EmailFormatFilter())
    filter_manager.add_filter(EmailDomainFilter())
    
    # Añadir filtros para la contraseña
    filter_manager.add_filter(PasswordLengthFilter())
    filter_manager.add_filter(PasswordNumberFilter())
    filter_manager.add_filter(PasswordSpecialCharFilter())
        
    # Solicitar credenciales al usuario
    print("=== Sistema de Autenticación ===")
    
    while True:
        email = input("Correo electrónico: ")
        password = input("Contraseña: ")
        
        # Preparar la solicitud
        request = {'email': email, 'password': password}
        
        # Procesar la solicitud
        result = filter_manager.process_request(request)
        
        # Mostrar el resultado
        if result['success']:
            print(f"\n✅ {result['message']}")
            break
        else:
            print("\n❌ La validación ha fallado:")
            for error in result['errors']:
                print(f"  - {error}")
            print("\nPor favor, inténtelo de nuevo.\n")

if __name__ == "__main__":
    main()