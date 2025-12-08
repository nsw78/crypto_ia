# src/connectors/coingecko_api.py

import requests
from typing import Optional, Dict, List

class CoinGeckoAPI:
    """Cliente para interagir com a API do CoinGecko (gratuita)."""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_coin_price(self, coin_id: str, vs_currency: str = "usd") -> Optional[float]:
        """
        Busca o preço atual de uma criptomoeda.
        
        Args:
            coin_id: ID da moeda no CoinGecko (ex: 'bitcoin', 'ethereum')
            vs_currency: Moeda de referência (ex: 'usd', 'brl')
            
        Returns:
            Preço atual ou None
        """
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': vs_currency,
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if coin_id in data:
                return data[coin_id][vs_currency]
            
            return None
        except Exception as e:
            print(f"Erro ao buscar preço: {e}")
            return None
    
    def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        """
        Busca dados detalhados de uma criptomoeda.
        
        Returns:
            Dicionário com preço, volume, market cap, etc.
        """
        url = f"{self.base_url}/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'true',
            'developer_data': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            return {
                'name': data.get('name'),
                'symbol': data.get('symbol', '').upper(),
                'current_price': data['market_data']['current_price']['usd'],
                'market_cap': data['market_data']['market_cap']['usd'],
                'market_cap_rank': data.get('market_cap_rank'),
                'total_volume': data['market_data']['total_volume']['usd'],
                'price_change_24h': data['market_data']['price_change_percentage_24h'],
                'price_change_7d': data['market_data']['price_change_percentage_7d'],
                'price_change_30d': data['market_data']['price_change_percentage_30d'],
                'ath': data['market_data']['ath']['usd'],
                'ath_change_percentage': data['market_data']['ath_change_percentage']['usd'],
                'atl': data['market_data']['atl']['usd'],
                'circulating_supply': data['market_data'].get('circulating_supply'),
                'total_supply': data['market_data'].get('total_supply'),
                'max_supply': data['market_data'].get('max_supply'),
            }
        except Exception as e:
            print(f"Erro ao buscar dados da moeda: {e}")
            return None
    
    def get_trending_coins(self) -> List[Dict]:
        """Busca as moedas em alta no momento."""
        url = f"{self.base_url}/search/trending"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            trending = []
            for item in data.get('coins', [])[:10]:
                coin = item['item']
                trending.append({
                    'id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'market_cap_rank': coin.get('market_cap_rank'),
                    'price_btc': coin.get('price_btc')
                })
            
            return trending
        except Exception as e:
            print(f"Erro ao buscar trending: {e}")
            return []
    
    def search_coin(self, query: str) -> Optional[str]:
        """
        Busca uma moeda por nome ou símbolo.
        
        Returns:
            ID da moeda no CoinGecko ou None
        """
        url = f"{self.base_url}/search"
        params = {'query': query}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('coins') and len(data['coins']) > 0:
                return data['coins'][0]['id']
            
            return None
        except Exception as e:
            print(f"Erro ao buscar moeda: {e}")
            return None
    
    def get_contract_info(self, platform: str, contract_address: str) -> Optional[Dict]:
        """
        Busca informações de uma moeda pelo endereço do contrato.
        
        Args:
            platform: 'ethereum', 'binance-smart-chain', etc.
            contract_address: Endereço do contrato
            
        Returns:
            Dados da moeda ou None
        """
        url = f"{self.base_url}/coins/{platform}/contract/{contract_address}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'symbol': data.get('symbol', '').upper(),
                    'current_price': data['market_data']['current_price']['usd'],
                    'market_cap': data['market_data']['market_cap'].get('usd'),
                    'total_volume': data['market_data']['total_volume'].get('usd'),
                    'price_change_24h': data['market_data'].get('price_change_percentage_24h'),
                    'liquidity_score': data.get('liquidity_score'),
                    'community_score': data.get('community_score')
                }
            
            return None
        except Exception as e:
            print(f"Erro ao buscar info do contrato: {e}")
            return None

# Instância global
coingecko = CoinGeckoAPI()

