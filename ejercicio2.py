from abc import ABC, abstractmethod
import json
import requests
from typing import Dict, Any

API_URL = "https://api-inference.huggingface.co/models/"

# Clase base abstracta LLM
class LLM(ABC):
    @abstractmethod
    def generate_summary(self, text: str, input_lang: str, output_lang: str, model: str) -> str:
        """Método abstracto para generar un resumen de texto"""
        pass

# Implementación concreta del LLM básico
class BasicLLM(LLM):
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.api_url = API_URL
    
    def generate_summary(self, text: str, input_lang: str, output_lang: str, model: str) -> str:
        """Genera un resumen utilizando el modelo LLM especificado"""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": text, "parameters": {"max_length": 150, "min_length": 50}}
        
        response = requests.post(
            f"{self.api_url}{model}",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            # La respuesta puede variar según el modelo, pero generalmente es una lista con un elemento
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "summary_text" in result[0]:
                    return result[0]["summary_text"]
                elif isinstance(result[0], dict) and "generated_text" in result[0]:
                    return result[0]["generated_text"]
            return str(result)
        else:
            return f"Error al generar resumen: {response.text}"

# Decorador base
class LLMDecorator(LLM):
    def __init__(self, llm: LLM):
        self.llm = llm
    
    @abstractmethod
    def generate_summary(self, text: str, input_lang: str, output_lang: str, model: str) -> str:
        """Delega la generación del resumen al componente decorado"""
        pass

# Decorador concreto para traducción
class TranslationDecorator(LLMDecorator):
    def __init__(self, llm: LLM, translation_model: str, api_token: str):
        super().__init__(llm)
        self.translation_model = translation_model
        self.api_token = api_token
        self.api_url = API_URL
    
    def generate_summary(self, text: str, input_lang: str, output_lang: str, model: str) -> str:
        """Genera un resumen y lo traduce al idioma especificado"""
        summary = self.llm.generate_summary(text, input_lang, output_lang, model)

        # Traducir el resumen
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": summary}
        
        response = requests.post(
            f"{self.api_url}{self.translation_model}",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]["translation_text"]
            return str(result)
        else:
            return f"Error al traducir: {response.text}"

# Decorador concreto para expansión
class ExpansionDecorator(LLMDecorator):
    def __init__(self, llm: LLM, expansion_model: str, api_token: str):
        super().__init__(llm)
        self.expansion_model = expansion_model
        self.api_token = api_token
        self.api_url = API_URL
    
    def generate_summary(self, text: str, input_lang: str, output_lang: str, model: str) -> str:
        """Genera un resumen y lo expande con detalles adicionales"""
        summary = self.llm.generate_summary(text, input_lang, output_lang, model)
        
        prompt = f"Expande: {summary[:100]}"  # Limitar el texto para evitar exceder límites
        
        # Expandir el resumen con truncación
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "truncation": "longest_first",
                "max_length": 128  # Asegurar que no excedemos el límite del modelo
            }
        }

        response = requests.post(
            f"{self.api_url}{self.expansion_model}",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    expanded_text = result[0]["generated_text"]
                else:
                    expanded_text = str(result[0])
            else:
                expanded_text = str(result)
            
            return f"Resumen original: {summary}\n\nExpansión: {expanded_text}"
        else:
            return f"Error al expandir: {response.text}"


# Función para cargar la configuración desde un archivo JSON
def load_config(config_file: str) -> Dict[str, Any]:
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        exit(1)

# Código cliente
def main():
    
    # Leer la configuración desde un archivo JSON
    config = load_config("config.json")
    
    # Obtener parámetros de configuración
    text = config["texto"]
    input_lang = config["input_lang"]
    output_lang = config["output_lang"]
    model_llm = config["model_llm"]
    model_translation = config["model_translation"]
    model_expansion = config["model_expansion"]
    
    # Token de API de Hugging Face (en un entorno real debería estar en una variable de entorno)
    api_token = "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"
    
    # Crear el LLM básico
    basicllm = BasicLLM(api_token)
    print("## Resumen básico:")
    basic_summary = basicllm.generate_summary(text, input_lang, output_lang, model_llm)
    print(basic_summary)
    print("\n" + "-"*50 + "\n")
    
    # Crear LLM con decorador de traducción
    translatedllm = TranslationDecorator(basicllm, model_translation, api_token)
    print("## Resumen traducido:")
    translated_summary = translatedllm.generate_summary(text, input_lang, output_lang, model_llm)
    print(translated_summary)
    print("\n" + "-"*50 + "\n")
    
    # Crear LLM con decorador de expansión
    expandedllm = ExpansionDecorator(basicllm, model_expansion, api_token)
    print("## Resumen expandido:")
    expanded_summary = expandedllm.generate_summary(text, input_lang, output_lang, model_llm)
    print(expanded_summary)
    print("\n" + "-"*50 + "\n")
    
    # Crear LLM con ambos decoradores (primero traducir, luego expandir)
    combinedllm = ExpansionDecorator(translatedllm, model_expansion, api_token)
    print("## Resumen traducido y expandido:")
    combined_summary = combinedllm.generate_summary(text, input_lang, output_lang, model_llm)
    print(combined_summary)

if __name__ == "__main__":
    main()