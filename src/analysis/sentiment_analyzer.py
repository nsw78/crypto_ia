# src/analysis/sentiment_analyzer.py

from src.connectors import news_api
from src.llm.llm_client import LLMClient
from src.llm.prompts import get_market_sentiment_prompt

def analyze_sentiment(asset: str) -> str:
    """
    Realiza a análise de sentimento de mercado para um ativo.

    1. Busca as últimas notícias e menções.
    2. Gera um prompt de análise.
    3. Envia o prompt para o LLM e retorna a resposta.
    """
    # 1. Buscar notícias (atualmente simulado)
    headlines = news_api.get_latest_news(asset)
    if not headlines:
        return f"Não foi possível encontrar notícias recentes sobre {asset}."

    # 2. Gerar o prompt de análise
    prompt = get_market_sentiment_prompt(headlines, asset)

    # 3. Enviar para o LLM
    llm_client = LLMClient()
    analysis_result = llm_client.generate_response(prompt)

    return analysis_result
