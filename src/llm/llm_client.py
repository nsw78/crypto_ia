# src/llm/llm_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class LLMClient:
    """
    Um cliente para interagir com um Grande Modelo de Linguagem (LLM).
    Este exemplo usa a API da OpenAI, mas pode ser adaptado para outros provedores
    ou para modelos locais como Ollama.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API da OpenAI não foi encontrada. Defina a variável de ambiente OPENAI_API_KEY.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, prompt: str, model: str = "gpt-4-turbo", temperature: float = 0.3) -> str:
        """
        Envia um prompt para o LLM e retorna a resposta.

        Args:
            prompt (str): O prompt a ser enviado para o modelo.
            model (str): O modelo a ser usado (ex: "gpt-4-turbo", "gpt-3.5-turbo").
            temperature (float): Controla a aleatoriedade da resposta. Valores mais baixos
                                 tornam a resposta mais determinística.

        Returns:
            str: A resposta gerada pelo modelo.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especialista em blockchain e finanças."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Em um app real, você usaria um logger aqui
            print(f"Erro ao chamar a API do LLM: {e}")
            return "Ocorreu um erro ao tentar gerar a análise. Por favor, verifique a chave da API e tente novamente."

# Exemplo de como você poderia adaptar para Ollama (comentado)
# import requests
# import json
#
# class OllamaClient:
#     def __init__(self, host='http://localhost:11434'):
#         self.host = host
#
#     def generate_response(self, prompt: str, model: str = "mistral"):
#         endpoint = f"{self.host}/api/generate"
#         payload = {
#             "model": model,
#             "prompt": prompt,
#             "stream": False
#         }
#         try:
#             response = requests.post(endpoint, data=json.dumps(payload))
#             response.raise_for_status()
#             return response.json()['response']
#         except Exception as e:
#             print(f"Erro ao conectar com o Ollama: {e}")
#             return "Erro ao conectar com o modelo local (Ollama)."
