# 🚀 Guia de Instalação e Configuração - Crypto IA Auditor

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Chave de API da OpenAI (obrigatório)
- Chaves de API opcionais: Etherscan, NewsAPI, Stripe

---

## ⚡ Instalação Rápida (5 minutos)

### 1. Clone ou acesse o projeto

```bash
cd CRYPTO_IA_PROJECT
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

### 5. Execute a aplicação

**Opção A - Versão SaaS completa (recomendado):**
```bash
streamlit run app_saas.py
```

**Opção B - Landing Page:**
```bash
streamlit run landing_page.py
```

**Opção C - Versão original simples:**
```bash
streamlit run app.py
```

🎉 **Pronto!** Acesse http://localhost:8501 no seu navegador.

---

## 🔑 Obtenção de API Keys

### OpenAI (OBRIGATÓRIO)

1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave (começa com `sk-proj-...`)
5. Cole no arquivo `.env`

**Custo:** ~$0.01-0.05 por análise (modelo gpt-4-turbo)

### Etherscan (OPCIONAL)

1. Acesse: https://etherscan.io/register
2. Crie uma conta
3. Vá em: https://etherscan.io/myapikey
4. Crie uma nova API key
5. Cole no arquivo `.env`

**Sem esta chave:** O sistema usará exemplos simulados

### NewsAPI (OPCIONAL)

1. Acesse: https://newsapi.org/register
2. Preencha o formulário
3. Copie a API key
4. Cole no arquivo `.env`

**Sem esta chave:** Análises de sentimento usarão notícias simuladas

### Stripe (OPCIONAL - apenas para monetização)

1. Acesse: https://dashboard.stripe.com/register
2. Crie uma conta
3. Use as chaves de **TEST** para desenvolvimento
4. Configure produtos e preços no dashboard
5. Adicione as chaves no `.env`

---

## 📁 Estrutura do Projeto

```
CRYPTO_IA_PROJECT/
│
├── app.py                  # Versão original simples
├── app_saas.py            # Versão SaaS completa ⭐
├── landing_page.py        # Landing page de vendas
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .env                  # Suas configurações (criar)
├── crypto_ia.db          # Banco de dados SQLite (criado automaticamente)
│
├── src/
│   ├── analysis/
│   │   ├── contract_analyzer.py      # Análise de contratos
│   │   ├── onchain_analyzer.py       # Análise de carteiras
│   │   ├── sentiment_analyzer.py     # Análise de sentimento
│   │   └── risk_scoring.py           # Sistema de score 0-100
│   │
│   ├── connectors/
│   │   ├── blockchain_api.py         # API blockchain genérica
│   │   ├── etherscan_api.py         # Integração Etherscan
│   │   ├── coingecko_api.py         # Preços e dados de moedas
│   │   └── news_api.py              # Notícias de cripto
│   │
│   ├── database/
│   │   └── db_manager.py            # Gerenciamento do banco
│   │
│   ├── llm/
│   │   ├── llm_client.py            # Cliente OpenAI
│   │   └── prompts.py               # Prompts de análise
│   │
│   ├── payment/
│   │   └── stripe_integration.py    # Integração Stripe
│   │
│   └── utils/
│       ├── helpers.py               # Funções auxiliares
│       └── pdf_generator.py         # Geração de relatórios
│
└── reports/                         # Relatórios gerados (criado automaticamente)
```

---

## 🎯 Funcionalidades Implementadas

### ✅ Sistema de Autenticação
- Login/Registro de usuários
- Sessões seguras
- Banco de dados SQLite

### ✅ Sistema de Créditos
- 3 análises grátis para novos usuários
- Sistema de planos (Free, Básico, Pro)
- Controle de consumo de créditos

### ✅ Análises Inteligentes
- **Contratos:** Detecta vulnerabilidades e padrões maliciosos
- **Carteiras:** Analisa comportamento on-chain
- **Sentimento:** Processa notícias e redes sociais

### ✅ Score de Risco Automático
- Pontuação 0-100
- Classificação: Baixo/Médio/Alto/Crítico
- Detecção de 20+ padrões de risco

### ✅ Dashboard Profissional
- Métricas em tempo real
- Histórico completo de análises
- Filtros e buscas

### ✅ Integração com APIs Reais
- Etherscan/BscScan (código-fonte de contratos)
- CoinGecko (preços e dados de mercado)
- NewsAPI (notícias em tempo real)

### ✅ Geração de Relatórios
- Relatórios em HTML profissionais
- Exportação futura para PDF
- Branding personalizado

### ✅ Sistema de Pagamentos
- Integração com Stripe preparada
- Webhooks configuráveis
- Portal do cliente

### ✅ Landing Page
- Design moderno e responsivo
- Seção de preços
- FAQs e depoimentos

---

## 🚀 Como Usar

### Criar uma Conta

1. Acesse `app_saas.py`
2. Clique em "Criar Conta"
3. Preencha seus dados
4. Você receberá 3 análises grátis!

### Realizar uma Análise

1. Faça login
2. Vá em "Nova Análise"
3. Escolha o tipo:
   - 🔍 Análise de Contrato
   - 🕵️ Análise de Carteira
   - 📊 Análise de Sentimento
4. Cole o endereço ou símbolo
5. Clique em "Analisar"
6. Aguarde 10-30 segundos

### Ver Histórico

1. Acesse "Histórico"
2. Filtre por tipo ou nível de risco
3. Clique em "Ver Detalhes" para análise completa

### Adquirir Mais Créditos

1. Vá em "Planos"
2. Escolha seu plano
3. Clique em "Assinar"
4. (Em produção: pagamento via Stripe)

---

## 🔧 Configurações Avançadas

### Customizar o Modelo de IA

Edite no arquivo `.env`:
```
LLM_MODEL=gpt-4-turbo      # Melhor qualidade
# LLM_MODEL=gpt-3.5-turbo  # Mais rápido e barato
```

### Ajustar Criatividade da IA

```
LLM_TEMPERATURE=0.3   # Conservador (recomendado para análises)
# LLM_TEMPERATURE=0.7 # Mais criativo
```

### Usar Modelos Locais (Ollama)

Descomente no arquivo `src/llm/llm_client.py`:
```python
# from ollama import Client
# client = Client(host='http://localhost:11434')
```

---

## 💡 Dicas de Uso

### Para Análises Mais Precisas

1. ✅ Configure as API keys (Etherscan, NewsAPI)
2. ✅ Use endereços verificados (com código-fonte)
3. ✅ Analise contratos em redes principais (Ethereum/BSC)
4. ✅ Compare múltiplas análises

### Economizar Créditos

- ⚡ Salve análises importantes no histórico
- ⚡ Use o score automático como primeira triagem
- ⚡ Analise apenas contratos/carteiras relevantes

### Maximizar Segurança

- 🔐 Sempre faça sua própria pesquisa (DYOR)
- 🔐 Use análises como uma camada extra de validação
- 🔐 Não invista baseado apenas em IA
- 🔐 Verifique informações em múltiplas fontes

---

## 🐛 Troubleshooting

### Erro: "No module named 'streamlit'"

```bash
pip install -r requirements.txt
```

### Erro: "OpenAI API key not found"

1. Verifique se o arquivo `.env` existe
2. Confirme que a chave começa com `sk-proj-`
3. Tente recarregar a aplicação

### Erro: "Database locked"

```bash
# Feche todas instâncias do app e rode:
rm crypto_ia.db
# Depois reinicie o app (ele recria o banco)
```

### Análises muito lentas

- Use `gpt-3.5-turbo` em vez de `gpt-4-turbo`
- Verifique sua conexão com internet
- OpenAI pode estar com alta demanda

### Erro ao buscar contratos reais

- Verifique se ETHERSCAN_API_KEY está configurado
- Confirme que o endereço está correto
- Alguns contratos não têm código verificado

---

## 📈 Próximos Passos (Roadmap)

### Fase 1 - Melhorias Imediatas
- [ ] Deploy em Streamlit Cloud
- [ ] Integração Stripe real
- [ ] Conversão de relatórios para PDF
- [ ] Sistema de alertas por email

### Fase 2 - Features Avançadas
- [ ] API REST pública
- [ ] Suporte a mais blockchains (Polygon, Arbitrum)
- [ ] Análise de NFTs
- [ ] Integração com wallets (MetaMask)

### Fase 3 - Escala
- [ ] Dashboard de administrador
- [ ] Sistema de afiliados
- [ ] White-label para empresas
- [ ] Mobile app

---

## 💰 Modelo de Monetização

### Plano Grátis
- 3 análises gratuitas
- Perfeito para testar

### Plano Básico - $49/mês
- 20 análises/mês
- Todas funcionalidades
- Suporte email

### Plano Pro - $199/mês
- 100 análises/mês
- Relatórios PDF
- API de acesso
- Suporte prioritário

### Enterprise - Customizado
- Análises ilimitadas
- White-label
- SLA garantido
- Suporte dedicado

---

## 📞 Suporte

**Desenvolvedor:** Nelson Walcow  
**Email:** nwalcow@gmail.com  
**GitHub:** [Seu GitHub]

---

## 📄 Licença

MIT License - Consulte o arquivo LICENSE

---

## ⚠️ Disclaimer

Esta ferramenta fornece análises automatizadas e não constitui aconselhamento financeiro. 
Sempre faça sua própria pesquisa (DYOR) antes de investir em qualquer ativo digital.

---

## 🎉 Parabéns!

Você agora tem um **SaaS completo de auditoria de contratos inteligentes**!

**Próximo passo:** Comece a analisar contratos e ganhe dinheiro!

```bash
streamlit run app_saas.py
```

🚀 **Boa sorte e bons negócios!**

