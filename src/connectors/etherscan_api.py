# src/connectors/etherscan_api.py

import requests
import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()

class EtherscanAPI:
    """Cliente para interagir com a API do Etherscan."""
    
    def __init__(self):
        self.api_key = os.getenv("ETHERSCAN_API_KEY", "")
        self.base_url = "https://api.etherscan.io/api"
        self.bsc_url = "https://api.bscscan.com/api"
    
    def get_contract_source_code(self, contract_address: str, network: str = "eth") -> Optional[Dict]:
        """
        Busca o código-fonte verificado de um contrato.
        
        Args:
            contract_address: Endereço do contrato
            network: 'eth' para Ethereum ou 'bsc' para Binance Smart Chain
            
        Returns:
            Dicionário com código-fonte e metadados ou None
        """
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': contract_address,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1' and data['result'][0]['SourceCode']:
                result = data['result'][0]
                return {
                    'source_code': result['SourceCode'],
                    'contract_name': result['ContractName'],
                    'compiler_version': result['CompilerVersion'],
                    'optimization': result['OptimizationUsed'],
                    'abi': result['ABI']
                }
            
            return None
        except Exception as e:
            print(f"Erro ao buscar código-fonte: {e}")
            return None
    
    def get_contract_abi(self, contract_address: str, network: str = "eth") -> Optional[str]:
        """Busca o ABI de um contrato."""
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': contract_address,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                return data['result']
            
            return None
        except Exception as e:
            print(f"Erro ao buscar ABI: {e}")
            return None
    
    def get_transactions(self, address: str, network: str = "eth", limit: int = 100) -> List[Dict]:
        """
        Busca transações normais de um endereço.
        
        Returns:
            Lista de transações
        """
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': limit,
            'sort': 'desc',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                return data['result']
            
            return []
        except Exception as e:
            print(f"Erro ao buscar transações: {e}")
            return []
    
    def get_token_transfers(self, address: str, network: str = "eth", limit: int = 100) -> List[Dict]:
        """Busca transferências de tokens ERC-20."""
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'page': 1,
            'offset': limit,
            'sort': 'desc',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                return data['result']
            
            return []
        except Exception as e:
            print(f"Erro ao buscar transferências de tokens: {e}")
            return []
    
    def get_internal_transactions(self, address: str, network: str = "eth", limit: int = 100) -> List[Dict]:
        """Busca transações internas (interações com contratos)."""
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'account',
            'action': 'txlistinternal',
            'address': address,
            'page': 1,
            'offset': limit,
            'sort': 'desc',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                return data['result']
            
            return []
        except Exception as e:
            print(f"Erro ao buscar transações internas: {e}")
            return []
    
    def get_balance(self, address: str, network: str = "eth") -> Optional[float]:
        """Retorna o saldo em ETH/BNB de um endereço."""
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                # Converte de Wei para ETH/BNB
                balance_wei = int(data['result'])
                balance_eth = balance_wei / 1e18
                return balance_eth
            
            return None
        except Exception as e:
            print(f"Erro ao buscar saldo: {e}")
            return None
    
    def is_contract(self, address: str, network: str = "eth") -> bool:
        """Verifica se o endereço é um contrato."""
        code = self.get_contract_code(address, network)
        return code is not None and code != "0x"
    
    def get_contract_code(self, address: str, network: str = "eth") -> Optional[str]:
        """Busca o bytecode de um contrato."""
        url = self.base_url if network == "eth" else self.bsc_url
        
        params = {
            'module': 'proxy',
            'action': 'eth_getCode',
            'address': address,
            'tag': 'latest',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'result' in data:
                return data['result']
            
            return None
        except Exception as e:
            print(f"Erro ao buscar código do contrato: {e}")
            return None

# Instância global
etherscan = EtherscanAPI()

