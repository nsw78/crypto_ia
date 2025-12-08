# 🔐 Crypto IA Auditor - SaaS Completo

**Auditoria Inteligente de Contratos com IA**

Proteja seus investimentos contra rug pulls, honeypots e vulnerabilidades com análises automatizadas por Inteligência Artificial.

**Autor:** Nelson Walcow  
**E-mail:** nwalcow@gmail.com

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-FF4B4B.svg)](https://streamlit.io)

---

## 🎯 Visão Geral

**Crypto IA Auditor** é um **SaaS completo e monetizável** para análise de contratos inteligentes, carteiras on-chain e sentimento de mercado. 

Combina:
- 🤖 **IA Avançada** (GPT-4) para análises profundas
- 📊 **Score de Risco** automático (0-100)
- 🔍 **APIs Reais** (Etherscan, CoinGecko, NewsAPI)
- 💼 **Sistema Completo** de autenticação, créditos e pagamentos

---

## ⚡ Início Rápido (5 minutos)

```bash
# 1. Crie o arquivo .env (copie de env_example.txt)
OPENAI_API_KEY=sua-chave-aqui

# 2. Ative o ambiente virtual
venv\Scripts\activate

# 3. Instale dependências (se necessário)
pip install -r requirements.txt

# 4. Execute o SaaS
streamlit run app_saas.py

# 5. Acesse http://localhost:8501
```

**📖 Leia:** `START_HERE.txt` para instruções detalhadas

---

## ✨ Funcionalidades Principais

### 🔍 Análise de Contratos Inteligentes
- Detecta vulnerabilidades e padrões maliciosos
- Score de risco 0-100 automático
- Identifica rug pulls e honeypots
- Análise de código real via Etherscan/BscScan
- Relatórios profissionais em HTML

### 🕵️ Análise de Carteiras On-Chain
- Histórico completo de transações
- Detecção de comportamentos suspeitos
- Identificação de mixers e scams
- Análise comportamental com IA

### 📊 Análise de Sentimento
- Processa notícias em tempo real
- Classificação: Positivo/Negativo/Neutro
- Identifica temas e narrativas
- Integração com NewsAPI

### 💼 Sistema SaaS Completo
- ✅ Autenticação e registro
- ✅ Sistema de créditos (3 grátis)
- ✅ Dashboard profissional
- ✅ Histórico com filtros
- ✅ Planos: Free, Básico ($49), Pro ($199)
- ✅ Integração com Stripe
- ✅ Landing page de vendas

---

## 🏗️ Arquitetura do Projeto

### Diagrama da Arquitetura

```
+-------------------------------+
|          Streamlit            |
|             App               |
+---------------+---------------+
                |
                v
+-------------------------------+
|         Analysis Module        |
| - Contratos                   |
| - Carteiras                   |
+---------------+---------------+
                |
                v
+-------------------------------+
|        Connectors Module      |
| - Etherscan API               |
| - News API                    |
+---------------+---------------+
                |
                v
+-------------------------------+
|           LLM Module          |
| - Prompts                     |
| - Cliente LLM                 |
+---------------+---------------+
                |
                v
+-------------------------------+
|          Utils Module         |
| - Validadores                 |
| - Normalização                |
+-------------------------------+
```

---

## Diagrama UML (versão limpa)

### Componentes Principais (UML Logical View)

```
App (Streamlit)
 - render_ui()
 - handle_inputs()
 - orchestrate_analysis()

Analysis
 - ContractAnalyzer
   - analyze_contract(code)
 - WalletAnalyzer
   - analyze_wallet(address)

Connectors
 - EtherscanConnector
   - get_transactions(address)
 - NewsConnector
   - get_news(asset)

LLM
 - PromptBuilder
   - build_prompt(type, data)
 - LLMClient
   - get_completion(prompt)

Utils
 - validate_address()
 - sanitize_code()
 - format_output()
```

---

## 🎯 Score de Risco (0-100)

Sistema automatizado que analisa:

- ✅ Funções perigosas (selfdestruct, delegatecall)
- ✅ Funções privilegiadas (onlyOwner, withdraw)
- ✅ Padrões de honeypot e rug pull
- ✅ Complexidade de código
- ✅ Bibliotecas de segurança (OpenZeppelin)
- ✅ Comportamento de carteiras

**Classificação:**
- 0-20: BAIXO (verde)
- 21-45: MÉDIO (amarelo)
- 46-70: ALTO (laranja)
- 71-100: CRÍTICO (vermelho)

---

## 📁 Estrutura do Projeto

```
CRYPTO_IA_PROJECT/
├── app_saas.py              # 🚀 App SaaS completo
├── landing_page.py          # 💼 Landing page de vendas
├── app.py                   # 📱 Versão original simples
├── START_HERE.txt           # ⚡ Comece aqui!
├── SETUP.md                 # 📖 Guia completo
├── MONETIZATION_PLAN.md     # 💰 Plano de negócio
│
├── src/
│   ├── analysis/            # Módulos de análise
│   │   ├── contract_analyzer.py
│   │   ├── onchain_analyzer.py
│   │   ├── sentiment_analyzer.py
│   │   └── risk_scoring.py  # Sistema de score
│   │
│   ├── connectors/          # APIs externas
│   │   ├── etherscan_api.py
│   │   ├── coingecko_api.py
│   │   └── news_api.py
│   │
│   ├── database/            # Banco de dados
│   │   └── db_manager.py
│   │
│   ├── payment/             # Stripe
│   │   └── stripe_integration.py
│   │
│   ├── llm/                 # IA
│   │   ├── llm_client.py
│   │   └── prompts.py
│   │
│   └── utils/               # Utilidades
│       ├── helpers.py
│       └── pdf_generator.py
│
└── crypto_ia.db             # Banco SQLite
```

---

## 🔑 Configuração de APIs

### Obrigatório:
- **OpenAI:** https://platform.openai.com/api-keys

### Opcional (Melhora análises):
- **Etherscan:** https://etherscan.io/myapikey
- **NewsAPI:** https://newsapi.org/register
- **Stripe:** https://dashboard.stripe.com/apikeys

**Arquivo:** Crie `.env` baseado em `env_example.txt`

---

## 🚀 Como Executar

### Versão SaaS (Recomendado):
```bash
streamlit run app_saas.py
```

### Landing Page:
```bash
streamlit run landing_page.py
```

### Versão Original:
```bash
streamlit run app.py
```

---

## 💰 Modelo de Monetização

### Planos Implementados:

| Plano | Preço | Análises/mês | Features |
|-------|-------|--------------|----------|
| **Free** | $0 | 3 | Todas funcionalidades básicas |
| **Básico** | $49 | 20 | + Análise de sentimento |
| **Pro** | $199 | 100 | + PDF, API, Suporte prioritário |
| **Enterprise** | Custom | Ilimitado | + White-label, SLA, Dedicado |

### Projeção de Receita (Ano 1):
- **Mês 3:** $500-1k MRR
- **Mês 6:** $5k MRR
- **Mês 12:** $20k-30k MRR

📖 **Veja:** `MONETIZATION_PLAN.md` para estratégias completas

---

## 📈 Roadmap

### ✅ Fase 1 – MVP (CONCLUÍDO)
- [x] App Streamlit básico
- [x] Módulos de análise
- [x] LLM integrado

### ✅ Fase 2 – Integrações Reais (CONCLUÍDO)
- [x] Etherscan API
- [x] CoinGecko API
- [x] NewsAPI
- [x] Banco de dados SQLite

### ✅ Fase 3 – IA Avançada (CONCLUÍDO)
- [x] Score de risco automático (0-100)
- [x] Detecção de 20+ padrões
- [x] Prompts contextualizados

### ✅ Fase 4 – SaaS Completo (CONCLUÍDO)
- [x] Sistema de autenticação
- [x] Dashboard profissional
- [x] Sistema de créditos e planos
- [x] Integração Stripe

### ✅ Fase 5 – Comercial (CONCLUÍDO)
- [x] Landing page
- [x] Geração de relatórios
- [x] Plano de monetização
- [x] Documentação completa

### ⏳ Fase 6 – Próximos Passos
- [ ] Deploy em produção
- [ ] Conversão PDF real
- [ ] API REST pública
- [ ] Mais blockchains (Polygon, Arbitrum)
- [ ] Mobile app

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **SQLite** - Banco de dados
- **OpenAI GPT-4** - Análise com IA
- **Streamlit** - Framework web

### APIs Integradas
- **Etherscan/BscScan** - Dados blockchain
- **CoinGecko** - Preços e mercado
- **NewsAPI** - Notícias crypto
- **Stripe** - Pagamentos

### Principais Bibliotecas
- `streamlit==1.51.0` - Interface web
- `openai==2.8.1` - Cliente OpenAI
- `web3==7.14.0` - Interação blockchain
- `requests==2.32.5` - HTTP requests
- `python-dotenv==1.2.1` - Variáveis ambiente

---

## 📊 Exemplos de Uso

### Analisar Contrato
```python
from src.analysis.contract_analyzer import analyze_contract

result = analyze_contract("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")
print(f"Score: {result['risk_score']}/100")
print(f"Nível: {result['risk_level']}")
```

### Analisar Carteira
```python
from src.analysis.onchain_analyzer import analyze_wallet

result = analyze_wallet("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae")
print(result['analysis_text'])
```

---

## 🎓 Casos de Uso

### Para Traders e Investidores
- Verificar contratos antes de investir
- Evitar rug pulls e scams
- Análise rápida de novos tokens
- Due diligence automatizada

### Para Desenvolvedores
- Pre-audit antes de deploys
- Identificar vulnerabilidades
- Aprender com análises
- Melhorar segurança do código

### Para Projetos e DAOs
- Auditar contratos de competidores
- Validar parcerias
- Monitorar ecossistema
- Relatórios para investidores

---

## 📈 Métricas do Sistema

Quando rodando em produção, você terá acesso a:

- 📊 Total de análises realizadas
- 👥 Usuários ativos
- 💰 MRR (Monthly Recurring Revenue)
- 📉 Taxa de churn
- ⚠️ Alertas de alto risco emitidos
- 🔥 Contratos mais analisados

---

## 🔒 Segurança

- ✅ Senhas com hash SHA-256
- ✅ Sessões seguras
- ✅ Validação de inputs
- ✅ SQL injection protegido
- ✅ API keys em variáveis de ambiente
- ✅ Rate limiting preparado

---

## 🧪 Testes

### Testar Localmente
```bash
# Executar app
streamlit run app_saas.py

# Testar com contratos conhecidos
# Uniswap: 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
# DAI: 0x6B175474E89094C44Da98b954EedeAC495271d0F
```

### Endereços de Teste
- **Baixo Risco:** Contratos verificados de projetos estabelecidos
- **Alto Risco:** Contratos com funções privilegiadas não documentadas

---

## 📚 Documentação Completa

- 📖 `START_HERE.txt` - Início rápido (5 min)
- 📖 `SETUP.md` - Instalação completa
- 📖 `QUICK_START.md` - Guia detalhado
- 📖 `MONETIZATION_PLAN.md` - Estratégias de receita
- 📖 `IMPLEMENTATION_SUMMARY.md` - Tudo que foi implementado

---

## 🤝 Contribuindo

Este é um projeto comercial, mas sugestões são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📝 Changelog

### [2.0.0] - 2025-12-08 ✨ MAJOR UPDATE
**Implementado:**
- Sistema completo de autenticação
- Score de risco automático (0-100)
- Dashboard profissional
- Sistema de créditos e planos
- Integração com APIs reais
- Geração de relatórios HTML
- Integração com Stripe
- Landing page de vendas
- Documentação completa

### [0.3.0] - 2025-11-21
- Diagrama UML e Arquitetura
- README profissional

### [0.2.0] - 2025-11-20
- Estrutura de módulos
- Protótipo Streamlit

### [0.1.0] - 2025-11-18
- Estrutura inicial

---

## ⚠️ Disclaimer

Esta ferramenta fornece análises automatizadas e **não constitui aconselhamento financeiro**. Sempre faça sua própria pesquisa (DYOR) antes de investir em qualquer ativo digital.

---

## 📞 Suporte e Contato

**Desenvolvedor:** Nelson Walcow  
**Email:** nwalcow@gmail.com  
**Projeto:** Crypto IA Auditor

**Precisa de ajuda?**
- 📖 Leia a documentação em `/SETUP.md`
- 🚀 Siga o guia em `/START_HERE.txt`
- 💰 Veja estratégias em `/MONETIZATION_PLAN.md`

---

## 📄 Licença

MIT License - Consulte o arquivo `LICENSE`

---

## 🎉 Comece Agora!

```bash
# 1. Configure
echo OPENAI_API_KEY=sua-chave > .env

# 2. Execute
streamlit run app_saas.py

# 3. Acesse
http://localhost:8501
```

**🚀 Você está pronto para lançar seu SaaS de auditoria de contratos!**

### Próximos Passos:
1. ✅ Rodar localmente
2. ⏳ Deploy em Streamlit Cloud (grátis)
3. ⏳ Marketing inicial
4. ⏳ Primeiros usuários pagantes
5. ⏳ Escalar para $10k-30k/mês

💪 **Boa sorte e bons negócios!**

