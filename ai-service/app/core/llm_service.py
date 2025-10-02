import os
import google.generativeai as genai

# Configura a chave de API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def generate_content(prompt: str) -> str:
    """
    Envia um prompt para o modelo Gemini e retorna a resposta.
    """
    #model = genai.GenerativeModel('gemini-1.5-flash')
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)

    return response.text

def list_available_models():
    models = genai.list_models()
    model_list = []
    for model in models:
        model_list.append(model.name)
    return model_list
