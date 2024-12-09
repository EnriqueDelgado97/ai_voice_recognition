import openai
import os
from dotenv import load_dotenv

load_dotenv()
# Configura tu clave de API
openai.api_key = os.getenv("API-KEY")

def procesar_texto_recibido(texto):
    """
    Envía texto reconocido desde imágenes o audio transcrito al asistente
    para extraer y estructurar la información en JSON.
    """
    messages = [
        {"role": "system", "content": """
You are an assistant that processes raw text input extracted from images or audio transcription. 
Your job is to extract and structure the following information:

1. Name (Nombre): The first name of the individual.
2. Last Names (Apellidos): The last names of the individual.
3. National ID (DNI): The complete National Identity Number, consisting of 8 digits followed by one letter.

Please ensure the DNI includes exactly 8 digits followed by a single letter, 
and handle both cases where the text is messy or well-formatted.

Respond only with a JSON object containing:
{
    "Nombre": "Extracted First Name",
    "Apellidos": "Extracted Last Names",
    "DNI": "Extracted National Identity Number"
}
        """},
        {"role": "user", "content": f"The following text needs to be processed: {texto}"}
    ]

    # Llamada al modelo
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Usa el modelo GPT-4 o el que tengas habilitado
        messages=messages,
        max_tokens=200,  # Ajusta los tokens si necesitas respuestas más largas
        temperature=0  # Respuestas más deterministas
    )

    # Extrae el contenido de la respuesta
    return response.choices[0].message.content

# Ejemplo de uso
texto_recibido = "Mi nombre es Enrique Delgado Aznar y mi DNI es 778-416-99Q."
resultado = procesar_texto_recibido(texto_recibido)
print(resultado)