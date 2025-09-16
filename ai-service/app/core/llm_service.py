import os
import google.generativeai as genai

# Configura a chave de API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def generate_content(prompt: str) -> str:
    """
    Envia um prompt para o modelo Gemini e retorna a resposta.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text
