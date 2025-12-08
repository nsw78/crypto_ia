# src/analysis/risk_scoring.py

import re
from typing import Dict, Tuple, List

class RiskScorer:
    """Sistema de pontuação de risco para contratos inteligentes."""
    
    # Padrões de risco alto
    HIGH_RISK_PATTERNS = [
        (r'selfdestruct', 30, "Função selfdestruct encontrada - contrato pode ser destruído"),
        (r'delegatecall', 25, "DelegateCall encontrado - pode executar código arbitrário"),
        (r'suicide', 30, "Função suicide encontrada - contrato pode ser destruído"),
        (r'\.call\{value:', 20, "Call com valor encontrado - possível reentrada"),
        (r'tx\.origin', 15, "Uso de tx.origin - vulnerável a phishing"),
        (r'block\.timestamp', 10, "Dependência de timestamp - pode ser manipulado"),
        (r'blockhash', 10, "Uso de blockhash - previsibilidade"),
    ]
    
    # Padrões de funções privilegiadas
    PRIVILEGED_PATTERNS = [
        (r'onlyOwner', 15, "Modificador onlyOwner - funções privilegiadas"),
        (r'withdraw.*\(', 20, "Função de saque encontrada"),
        (r'transferOwnership', 15, "Função de transferência de propriedade"),
        (r'setFee|changeFee|updateFee', 15, "Pode alterar taxas dinamicamente"),
        (r'mint\(', 15, "Função de mint - pode criar tokens"),
        (r'burn\(', 10, "Função de burn - pode destruir tokens"),
        (r'pause|unpause', 15, "Função de pausa - pode congelar operações"),
        (r'blacklist|whitelist', 20, "Sistema de blacklist/whitelist"),
    ]
    
    # Padrões suspeitos
    SUSPICIOUS_PATTERNS = [
        (r'honeypot', 40, "Palavra 'honeypot' no código"),
        (r'rugpull|rug_pull', 50, "Referência a rug pull"),
        (r'hidden', 15, "Variável ou função 'hidden'"),
        (r'private.*key', 25, "Referência a chave privada"),
        (r'backdoor', 40, "Palavra 'backdoor' no código"),
    ]
    
    def __init__(self):
        self.risk_factors = []
        self.base_score = 0
    
    def analyze_contract_code(self, source_code: str) -> Tuple[int, str, List[str]]:
        """
        Analisa o código-fonte e retorna score de risco.
        
        Returns:
            Tuple (score, level, factors) onde:
            - score: 0-100 (0 = seguro, 100 = extremamente perigoso)
            - level: 'BAIXO', 'MÉDIO', 'ALTO', 'CRÍTICO'
            - factors: Lista de fatores de risco encontrados
        """
        self.risk_factors = []
        self.base_score = 0
        
        # Verifica se há código-fonte
        if not source_code or len(source_code.strip()) < 50:
            return 85, "CRÍTICO", ["Código-fonte não verificado ou indisponível"]
        
        # Remove comentários para análise mais precisa
        code_no_comments = self._remove_comments(source_code)
        
        # Análise de padrões de alto risco
        self._check_patterns(code_no_comments, self.HIGH_RISK_PATTERNS)
        
        # Análise de funções privilegiadas
        self._check_patterns(code_no_comments, self.PRIVILEGED_PATTERNS)
        
        # Análise de padrões suspeitos
        self._check_patterns(code_no_comments, self.SUSPICIOUS_PATTERNS)
        
        # Análises adicionais
        self._check_complexity(code_no_comments)
        self._check_security_features(code_no_comments)
        self._check_license(source_code)
        
        # Calcula score final (máximo 100)
        final_score = min(self.base_score, 100)
        
        # Determina nível de risco
        risk_level = self._get_risk_level(final_score)
        
        return final_score, risk_level, self.risk_factors
    
    def _check_patterns(self, code: str, patterns: List[Tuple]):
        """Verifica padrões de risco no código."""
        for pattern, score_penalty, description in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                self.base_score += score_penalty
                self.risk_factors.append(description)
    
    def _check_complexity(self, code: str):
        """Analisa a complexidade do código."""
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        # Código muito curto pode ser suspeito
        if len(non_empty_lines) < 50:
            self.base_score += 5
            self.risk_factors.append("Código muito simples - possível contrato proxy ou scam")
        
        # Código extremamente longo pode esconder comportamentos
        elif len(non_empty_lines) > 1000:
            self.base_score += 10
            self.risk_factors.append("Código muito extenso - dificulta auditoria")
        
        # Verifica funções muito longas
        function_pattern = r'function\s+\w+.*?\{(.*?)\n\s*\}'
        functions = re.findall(function_pattern, code, re.DOTALL)
        for func in functions:
            func_lines = [l for l in func.split('\n') if l.strip()]
            if len(func_lines) > 100:
                self.base_score += 5
                self.risk_factors.append("Função muito longa detectada")
                break
    
    def _check_security_features(self, code: str):
        """Verifica presença de recursos de segurança."""
        security_score_reduction = 0
        
        # Bônus por usar bibliotecas conhecidas
        if re.search(r'import.*OpenZeppelin', code, re.IGNORECASE):
            security_score_reduction += 10
            self.risk_factors.append("✓ Usa bibliotecas OpenZeppelin (positivo)")
        
        # Bônus por usar SafeMath
        if re.search(r'SafeMath|using\s+\w+\s+for\s+uint', code):
            security_score_reduction += 5
            self.risk_factors.append("✓ Usa SafeMath (positivo)")
        
        # Bônus por ter ReentrancyGuard
        if re.search(r'ReentrancyGuard|nonReentrant', code):
            security_score_reduction += 10
            self.risk_factors.append("✓ Proteção contra reentrada (positivo)")
        
        # Bônus por ter Pausable
        if re.search(r'Pausable', code):
            security_score_reduction += 5
            self.risk_factors.append("✓ Implementa Pausable (positivo)")
        
        # Aplica redução de score (não pode ser negativo)
        self.base_score = max(0, self.base_score - security_score_reduction)
    
    def _check_license(self, code: str):
        """Verifica presença de licença."""
        if not re.search(r'SPDX-License-Identifier', code):
            self.base_score += 5
            self.risk_factors.append("Sem identificador de licença SPDX")
    
    def _remove_comments(self, code: str) -> str:
        """Remove comentários do código."""
        # Remove comentários de linha única
        code = re.sub(r'//.*', '', code)
        # Remove comentários de múltiplas linhas
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code
    
    def _get_risk_level(self, score: int) -> str:
        """Determina o nível de risco baseado no score."""
        if score <= 20:
            return "BAIXO"
        elif score <= 45:
            return "MÉDIO"
        elif score <= 70:
            return "ALTO"
        else:
            return "CRÍTICO"
    
    def analyze_wallet_behavior(self, transaction_data: str) -> Tuple[int, str, List[str]]:
        """
        Analisa o comportamento de uma carteira baseado em transações.
        
        Returns:
            Tuple (score, level, factors)
        """
        self.risk_factors = []
        self.base_score = 0
        
        data_lower = transaction_data.lower()
        
        # Padrões suspeitos em transações
        if 'mixer' in data_lower or 'tornado' in data_lower:
            self.base_score += 30
            self.risk_factors.append("Uso de mixers (Tornado Cash ou similar)")
        
        if 'airdrop suspeito' in data_lower or 'scam' in data_lower:
            self.base_score += 20
            self.risk_factors.append("Tokens de airdrop suspeitos recebidos")
        
        if 'recém-criada' in data_lower or 'nova carteira' in data_lower:
            self.base_score += 15
            self.risk_factors.append("Interações com carteiras recém-criadas")
        
        if 'ilimitado' in data_lower or 'unlimited' in data_lower:
            self.base_score += 25
            self.risk_factors.append("Aprovações ilimitadas concedidas")
        
        if 'desconhecido' in data_lower or 'unknown' in data_lower:
            self.base_score += 15
            self.risk_factors.append("Interações com contratos desconhecidos")
        
        # Padrões positivos
        if 'staking' in data_lower:
            self.base_score -= 5
            self.risk_factors.append("✓ Uso de staking (positivo)")
        
        if len(self.risk_factors) == 0:
            self.base_score = 10
            self.risk_factors.append("Nenhum padrão suspeito detectado")
        
        final_score = max(0, min(self.base_score, 100))
        risk_level = self._get_risk_level(final_score)
        
        return final_score, risk_level, self.risk_factors

# Instância global
risk_scorer = RiskScorer()

