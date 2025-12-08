# src/connectors/blockchain_api.py

import time
from .etherscan_api import etherscan

def get_contract_source_code(contract_address: str, network: str = "eth") -> str:
    """
    Busca o código-fonte de um contrato usando Etherscan/BscScan API.
    """
    print(f"Buscando código-fonte para o contrato: {contract_address}...")
    
    # Tenta buscar código-fonte real da API
    contract_data = etherscan.get_contract_source_code(contract_address, network)
    
    if contract_data and contract_data['source_code']:
        return contract_data['source_code']
    
    # Fallback: Código de exemplo se não encontrar ou se API key não estiver configurada
    print("⚠️  Usando código de exemplo (configure ETHERSCAN_API_KEY para análises reais)")
    time.sleep(1)
    
    sample_code = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract RiskyToken {
        mapping(address => uint256) public balances;
        address public owner;
        uint256 public taxFee = 5; // Taxa de 5%

        event Transfer(address indexed from, address indexed to, uint256 value);

        constructor() {
            owner = msg.sender;
            balances[msg.sender] = 1000000 * 10**18;
        }

        function transfer(address to, uint256 value) public {
            uint256 fee = (value * taxFee) / 100;
            uint256 sendValue = value - fee;
            
            require(balances[msg.sender] >= value, "Saldo insuficiente");
            
            balances[msg.sender] -= value;
            balances[to] += sendValue;
            balances[owner] += fee; // Taxa vai para o proprietário
            
            emit Transfer(msg.sender, to, value);
        }

        // Função suspeita: O proprietário pode alterar a taxa a qualquer momento.
        function setTaxFee(uint256 newFee) public {
            require(msg.sender == owner, "Apenas o proprietário pode alterar a taxa");
            require(newFee <= 100, "A taxa não pode ser maior que 100%");
            taxFee = newFee;
        }

        // Função perigosa: O proprietário pode sacar todos os fundos do contrato.
        function withdrawEther() public {
            require(msg.sender == owner, "Apenas o proprietário");
            payable(owner).transfer(address(this).balance);
        }
    }
    """
    return sample_code

def get_wallet_transaction_history(wallet_address: str, network: str = "eth") -> str:
    """
    Busca o histórico de transações de uma carteira usando Etherscan/BscScan API.
    """
    print(f"Buscando histórico de transações para a carteira: {wallet_address}...")
    
    # Tenta buscar transações reais da API
    transactions = etherscan.get_transactions(wallet_address, network, limit=20)
    token_transfers = etherscan.get_token_transfers(wallet_address, network, limit=10)
    
    if transactions or token_transfers:
        history = "Histórico de Transações (Últimas 20):\n\n"
        
        # Transações normais
        if transactions:
            history += "Transações ETH/BNB:\n"
            for i, tx in enumerate(transactions[:10], 1):
                value_eth = int(tx['value']) / 1e18 if tx['value'] else 0
                tx_type = "Enviou" if tx['from'].lower() == wallet_address.lower() else "Recebeu"
                other_addr = tx['to'] if tx_type == "Enviou" else tx['from']
                history += f"{i}. {tx_type} {value_eth:.4f} ETH para/de {other_addr[:10]}...{other_addr[-6:]}\n"
        
        # Transferências de tokens
        if token_transfers:
            history += "\nTransferências de Tokens:\n"
            for i, tx in enumerate(token_transfers[:10], 1):
                value = int(tx['value']) / (10 ** int(tx.get('tokenDecimal', 18)))
                tx_type = "Enviou" if tx['from'].lower() == wallet_address.lower() else "Recebeu"
                history += f"{i}. {tx_type} {value:.2f} {tx['tokenSymbol']} ({tx['tokenName']})\n"
        
        return history
    
    # Fallback: Histórico de exemplo
    print("⚠️  Usando histórico de exemplo (configure ETHERSCAN_API_KEY para análises reais)")
    time.sleep(1)
    
    sample_history = f"""
    Histórico de Transações de Exemplo:
    
    - Transação 1: Enviou 0.5 ETH para 0x123...abc (Contrato de Staking)
    - Transação 2: Recebeu 10,000,000 SHIBA-INU-CLONE de 0xdef...456 (Airdrop suspeito)
    - Transação 3: Trocou 0.1 ETH por 500 ROCKETCOIN em um DEX desconhecido.
    - Transação 4: Enviou 0.01 ETH para Tornado.Cash Mixer.
    - Transação 5: Recebeu 2 ETH de uma carteira recém-criada (0x999...xyz).
    - Transação 6: Aprovou gasto ilimitado de ROCKETCOIN para um contrato desconhecido.
    """
    return sample_history
