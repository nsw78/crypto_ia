# src/utils/helpers.py

import re
from web3 import Web3

def is_valid_ethereum_address(address: str) -> bool:
    """
    Verifica se uma string é um endereço Ethereum válido, incluindo a validação
    de formato e checksum (EIP-55).
    """
    try:
        # A função is_address da Web3.py verifica o formato básico.
        # A função is_checksum_address verifica o checksum EIP-55.
        return Web3.is_address(address) and Web3.is_checksum_address(address)
    except:
        return Web3.is_address(address) # Fallback para endereços sem checksum
