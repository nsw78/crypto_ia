# src/connectors/news_api.py

import requests
import os
from typing import List, Dict
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class CryptoNewsAPI:
    """Cliente para buscar notícias de criptomoedas."""
    
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY", "")
        self.newsapi_url = "https://newsapi.org/v2/everything"
    
    def get_latest_news(self, asset: str, days: int = 7, max_results: int = 10) -> List[Dict]:
        """
        Busca notícias recentes sobre um ativo usando NewsAPI.
        
        Args:
            asset: Símbolo ou nome da criptomoeda
            days: Número de dias para buscar notícias
            max_results: Número máximo de resultados
            
        Returns:
            Lista de notícias
        """
        if not self.newsapi_key:
            # Fallback para notícias simuladas se não houver API key
            return self._get_simulated_news(asset)
        
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            'q': f'{asset} OR crypto OR cryptocurrency',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': max_results,
            'apiKey': self.newsapi_key
        }
        
        try:
            response = requests.get(self.newsapi_url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == 'ok':
                articles = []
                for article in data['articles']:
                    articles.append({
                        'title': article['title'],
                        'description': article.get('description', ''),
                        'source': article['source']['name'],
                        'published_at': article['publishedAt'],
                        'url': article['url']
                    })
                return articles
            
            return self._get_simulated_news(asset)
        except Exception as e:
            print(f"Erro ao buscar notícias: {e}")
            return self._get_simulated_news(asset)
    
    def _get_simulated_news(self, asset: str) -> List[Dict]:
        """Notícias simuladas caso a API não esteja disponível."""
        return [
            {
                'title': f'Reguladores dos EUA expressam preocupação com a centralização de {asset}',
                'description': 'Autoridades regulatórias levantam questões sobre governança.',
                'source': 'Crypto Regulation News',
                'published_at': datetime.now().isoformat(),
                'url': '#'
            },
            {
                'title': f'Gigante da tecnologia anuncia parceria para usar a rede {asset}',
                'description': 'Nova integração pode impulsionar adoção.',
                'source': 'Tech Daily',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'url': '#'
            },
            {
                'title': f'Análise On-Chain mostra grande acúmulo de {asset} por baleias',
                'description': 'Dados on-chain revelam movimentação significativa.',
                'source': 'Blockchain Analytics',
                'published_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'url': '#'
            },
            {
                'title': f'Relatório de segurança revela vulnerabilidade crítica no ecossistema {asset}',
                'description': 'Especialistas em segurança alertam para possíveis riscos.',
                'source': 'CyberSec Crypto',
                'published_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'url': '#'
            }
        ]
    
    def format_news_for_analysis(self, news_list: List[Dict]) -> str:
        """Formata a lista de notícias para análise da IA."""
        if not news_list:
            return "Nenhuma notícia recente encontrada."
        
        formatted = "Notícias Recentes:\n\n"
        for i, news in enumerate(news_list, 1):
            formatted += f"{i}. {news['title']}\n"
            if news.get('description'):
                formatted += f"   {news['description']}\n"
            formatted += f"   Fonte: {news['source']} | Data: {news['published_at'][:10]}\n\n"
        
        return formatted

# Instância global
news_api = CryptoNewsAPI()

# Função de compatibilidade com código antigo
def get_latest_news(asset: str) -> str:
    """Função wrapper para compatibilidade."""
    news_list = news_api.get_latest_news(asset)
    return news_api.format_news_for_analysis(news_list)
