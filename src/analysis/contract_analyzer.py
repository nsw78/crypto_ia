# src/analysis/contract_analyzer.py

from src.connectors import blockchain_api
from src.llm.llm_client import LLMClient
from src.llm.prompts import get_contract_analysis_prompt

def analyze_contract(contract_address: str) -> str:
    """
    Realiza a análise completa de um contrato inteligente.

    1. Busca o código-fonte do contrato.
    2. Gera um prompt de análise.
    3. Envia o prompt para o LLM e retorna a resposta.
    """
    # 1. Buscar o código-fonte (atualmente simulado)
    source_code = blockchain_api.get_contract_source_code(contract_address)
    if not source_code:
        return "Não foi possível encontrar o código-fonte para este contrato."

    # 2. Gerar o prompt de análise
    prompt = get_contract_analysis_prompt(source_code)

    # 3. Enviar para o LLM
    llm_client = LLMClient()
    analysis_result = llm_client.generate_response(prompt)

    return analysis_result
