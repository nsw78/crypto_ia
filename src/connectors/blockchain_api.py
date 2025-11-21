# src/connectors/blockchain_api.py

import time

# TODO: Substituir esta simulação por chamadas reais de API usando a biblioteca 'requests'.
# Você precisará de chaves de API para serviços como Etherscan, BscScan, etc.

def get_contract_source_code(contract_address: str) -> str:
    """
    Simula a busca do código-fonte de um contrato em um explorador de blocos.
    """
    print(f"Buscando código-fonte para o contrato: {contract_address}...")
    time.sleep(1) # Simula a latência da rede

    # Exemplo de código de contrato com uma vulnerabilidade e função suspeita
    # para que o LLM tenha o que analisar.
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

def get_wallet_transaction_history(wallet_address: str) -> str:
    """
    Simula a busca do histórico de transações de uma carteira.
    """
    print(f"Buscando histórico de transações para a carteira: {wallet_address}...")
    time.sleep(1)

    # Exemplo de histórico de transações para análise
    sample_history = f"""
    - Transação 1: Enviou 0.5 ETH para 0x123...abc (Contrato de Staking)
    - Transação 2: Recebeu 10,000,000 SHIBA-INU-CLONE de 0xdef...456 (Airdrop suspeito)
    - Transação 3: Trocou 0.1 ETH por 500 ROCKETCOIN em um DEX desconhecido.
    - Transação 4: Enviou 0.01 ETH para Tornado.Cash Mixer.
    - Transação 5: Recebeu 2 ETH de uma carteira recém-criada (0x999...xyz).
    - Transação 6: Aprovou gasto ilimitado de ROCKETCOIN para um contrato desconhecido.
    """
    return sample_history
