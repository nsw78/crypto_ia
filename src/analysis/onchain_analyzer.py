# src/analysis/onchain_analyzer.py

from src.connectors import blockchain_api
from src.llm.llm_client import LLMClient
from src.llm.prompts import get_wallet_analysis_prompt
from src.analysis.risk_scoring import risk_scorer
from typing import Dict

def analyze_wallet(wallet_address: str, network: str = "eth") -> Dict:
    """
    Realiza a análise completa de uma carteira.

    1. Busca o histórico de transações.
    2. Calcula score de risco baseado em comportamento.
    3. Gera análise detalhada com LLM.
    4. Retorna resultado completo.
    
    Returns:
        Dict com: analysis_text, risk_score, risk_level, risk_factors
    """
    # 1. Buscar o histórico de transações
    history = blockchain_api.get_wallet_transaction_history(wallet_address, network)
    if not history:
        return {
            'analysis_text': "Não foi possível encontrar o histórico de transações para esta carteira.",
            'risk_score': 50,
            'risk_level': 'MÉDIO',
            'risk_factors': ['Histórico não encontrado']
        }

    # 2. Calcular score de risco
    risk_score, risk_level, risk_factors = risk_scorer.analyze_wallet_behavior(history)

    # 3. Gerar o prompt de análise
    prompt = get_wallet_analysis_prompt(history, wallet_address, risk_score, risk_level)

    # 4. Enviar para o LLM
    llm_client = LLMClient()
    analysis_result = llm_client.generate_response(prompt)

    return {
        'analysis_text': analysis_result,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_factors': risk_factors
    }
