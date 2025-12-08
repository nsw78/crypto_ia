# src/llm/prompts.py

def get_contract_analysis_prompt(contract_code: str, risk_score: int = None, risk_level: str = None) -> str:
    """
    Gera o prompt para analisar um contrato inteligente em Solidity.
    """
    risk_context = ""
    if risk_score is not None and risk_level is not None:
        risk_context = f"""
    
    **CONTEXTO DE ANÁLISE AUTOMATIZADA:**
    Nosso sistema de análise automatizada já detectou um Score de Risco de {risk_score}/100 (Nível: {risk_level}).
    Use essa informação como referência, mas faça sua própria análise independente.
    """
    
    return f"""
    Você é um especialista em segurança de contratos inteligentes e auditor de blockchain.
    Sua tarefa é analisar o seguinte contrato em Solidity e fornecer um relatório detalhado.
    {risk_context}
    O relatório deve incluir:
    1.  **Resumo do Contrato**: Uma breve explicação do propósito do contrato em linguagem simples.
    2.  **Análise de Riscos (Veredito)**: Classifique o risco como BAIXO, MÉDIO, ALTO ou CRÍTICO. Justifique sua classificação.
    3.  **Vulnerabilidades Potenciais**: Identifique quaisquer vulnerabilidades conhecidas (ex: reentrancy, integer overflow, etc.).
    4.  **Funções Suspeitas (Potencial Rug Pull)**: Procure por funções que possam ser maliciosas, como:
        - Funções de mint ilimitado.
        - Funções que permitem ao proprietário drenar a liquidez.
        - Funções que podem impedir a venda (honeypot).
        - Cláusulas que permitem a alteração de taxas para 100%.
        - Centralização excessiva de poder no proprietário.
    5.  **Recomendações**: Sugira melhorias ou pontos de atenção para um desenvolvedor.

    Analise o seguinte contrato:
    ```solidity
    {contract_code}
    ```
    """

def get_wallet_analysis_prompt(wallet_history: str, wallet_address: str, risk_score: int = None, risk_level: str = None) -> str:
    """
    Gera o prompt para analisar o histórico de transações de uma carteira.
    """
    risk_context = ""
    if risk_score is not None and risk_level is not None:
        risk_context = f"""
    
    **CONTEXTO DE ANÁLISE AUTOMATIZADA:**
    Nosso sistema de análise comportamental detectou um Score de Risco de {risk_score}/100 (Nível: {risk_level}).
    Considere essa informação em sua análise.
    """
    
    return f"""
    Você é um analista de blockchain forense. Sua tarefa é analisar o histórico de transações de uma carteira para identificar padrões suspeitos.

    A carteira a ser analisada é: {wallet_address}
    {risk_context}
    O histórico de transações é o seguinte:
    {wallet_history}

    Com base nesses dados, forneça a seguinte análise:
    1.  **Resumo da Atividade**: Descreva o comportamento geral da carteira (ex: holder, trader frequente, interação com dApps, etc.).
    2.  **Detecção de Padrões Suspeitos**: Identifique atividades que possam indicar risco, como:
        - Interação com contratos conhecidos por golpes (scams).
        - Recebimento de fundos de mixers (ex: Tornado Cash).
        - Padrões de "pump and dump".
        - Transações muito rápidas e em série que podem indicar atividade de bot.
    3.  **Nível de Risco da Carteira**: Classifique o risco da carteira como BAIXO, MÉDIO, ALTO ou CRÍTICO, com base nos padrões detectados.
    4.  **Observações Adicionais**: Qualquer outra informação relevante que você possa extrair dos dados.
    """

def get_market_sentiment_prompt(news_headlines: str, asset: str) -> str:
    """
    Gera o prompt para analisar o sentimento do mercado a partir de notícias.
    """
    return f"""
    Você é um analista de mercado financeiro especializado em criptomoedas.
    Sua tarefa é analisar as seguintes manchetes de notícias e posts de redes sociais sobre o ativo '{asset}' e determinar o sentimento geral do mercado.

    As manchetes são:
    ---
    {news_headlines}
    ---

    Com base nessas informações, forneça:
    1.  **Sentimento Geral**: Classifique como POSITIVO, NEGATIVO ou NEUTRO.
    2.  **Justificativa**: Explique brevemente por que você chegou a essa conclusão, citando exemplos das manchetes.
    3.  **Principais Temas**: Identifique os 2-3 principais temas ou narrativas presentes nas notícias (ex: "preocupações regulatórias", "adoção institucional", "falha de segurança").
    """
