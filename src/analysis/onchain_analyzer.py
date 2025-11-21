# src/analysis/onchain_analyzer.py

from src.connectors import blockchain_api
from src.llm.llm_client import LLMClient
from src.llm.prompts import get_wallet_analysis_prompt

def analyze_wallet(wallet_address: str) -> str:
    """
    Realiza a análise completa de uma carteira.

    1. Busca o histórico de transações.
    2. Gera um prompt de análise.
    3. Envia o prompt para o LLM e retorna a resposta.
    """
    # 1. Buscar o histórico de transações (atualmente simulado)
    history = blockchain_api.get_wallet_transaction_history(wallet_address)
    if not history:
        return "Não foi possível encontrar o histórico de transações para esta carteira."

    # 2. Gerar o prompt de análise
    prompt = get_wallet_analysis_prompt(history, wallet_address)

    # 3. Enviar para o LLM
    llm_client = LLMClient()
    analysis_result = llm_client.generate_response(prompt)

    return analysis_result
