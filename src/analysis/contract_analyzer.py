# src/analysis/contract_analyzer.py

from src.connectors import blockchain_api
from src.llm.llm_client import LLMClient
from src.llm.prompts import get_contract_analysis_prompt
from src.analysis.risk_scoring import risk_scorer
from typing import Dict

def analyze_contract(contract_address: str, network: str = "eth") -> Dict:
    """
    Realiza a análise completa de um contrato inteligente.

    1. Busca o código-fonte do contrato.
    2. Calcula score de risco automatizado.
    3. Gera análise detalhada com LLM.
    4. Retorna resultado completo.
    
    Returns:
        Dict com: analysis_text, risk_score, risk_level, risk_factors
    """
    # 1. Buscar o código-fonte
    source_code = blockchain_api.get_contract_source_code(contract_address, network)
    if not source_code:
        return {
            'analysis_text': "Não foi possível encontrar o código-fonte para este contrato.",
            'risk_score': 85,
            'risk_level': 'CRÍTICO',
            'risk_factors': ['Código-fonte não verificado ou indisponível']
        }

    # 2. Calcular score de risco
    risk_score, risk_level, risk_factors = risk_scorer.analyze_contract_code(source_code)

    # 3. Gerar o prompt de análise com contexto de risco
    prompt = get_contract_analysis_prompt(source_code, risk_score, risk_level)

    # 4. Enviar para o LLM
    llm_client = LLMClient()
    analysis_result = llm_client.generate_response(prompt)

    return {
        'analysis_text': analysis_result,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_factors': risk_factors
    }
