# app_saas.py - Versão SaaS com Autenticação e Monetização

import streamlit as st
from datetime import datetime
from src.database.db_manager import db
from src.analysis.contract_analyzer import analyze_contract
from src.analysis.onchain_analyzer import analyze_wallet
from src.analysis.sentiment_analyzer import analyze_sentiment
from src.utils.helpers import is_valid_ethereum_address
from src.connectors.coingecko_api import coingecko
import os

# Configuração da página
st.set_page_config(
    page_title="Crypto IA Auditor - SaaS",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para UI profissional
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .risk-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .risk-low { background: #10b981; color: white; }
    .risk-medium { background: #f59e0b; color: white; }
    .risk-high { background: #ef4444; color: white; }
    .risk-critical { background: #7f1d1d; color: white; }
    .credit-badge {
        background: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
    }
    .plan-card {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .plan-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Funções de autenticação
def login_page():
    """Página de login."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<p class="main-header">🔐 Crypto IA Auditor</p>', unsafe_allow_html=True)
        st.markdown("### Login")
        
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("Login", use_container_width=True):
                user = db.authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos")
        
        with col_register:
            if st.button("Criar Conta", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("---")
        st.info("💡 **Demo:** Crie uma conta gratuita e receba 3 análises grátis!")

def register_page():
    """Página de registro."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<p class="main-header">📝 Criar Conta</p>', unsafe_allow_html=True)
        
        full_name = st.text_input("Nome Completo")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        password_confirm = st.text_input("Confirmar Senha", type="password")
        
        col_back, col_create = st.columns(2)
        
        with col_back:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        
        with col_create:
            if st.button("Criar Conta", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Preencha todos os campos")
                elif password != password_confirm:
                    st.error("As senhas não coincidem")
                elif len(password) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres")
                else:
                    user_id = db.create_user(email, password, full_name)
                    if user_id:
                        st.success("✅ Conta criada com sucesso! Você ganhou 3 análises grátis!")
                        st.balloons()
                        user = db.authenticate_user(email, password)
                        st.session_state.user = user
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("❌ Este email já está cadastrado")

def dashboard_page():
    """Dashboard principal após login."""
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {user['full_name'] or user['email']}")
        
        # Mostrar créditos
        credits = db.get_user_credits(user['id'])
        plan = user['plan'].upper()
        
        st.markdown(f'<div class="credit-badge">💎 {credits} Créditos</div>', unsafe_allow_html=True)
        st.markdown(f"**Plano:** {plan}")
        
        st.markdown("---")
        
        # Menu de navegação
        page = st.radio(
            "Menu",
            ["🏠 Dashboard", "🔍 Nova Análise", "📊 Histórico", "💳 Planos", "⚙️ Configurações"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'login'
            st.rerun()
    
    # Conteúdo principal baseado na página selecionada
    if page == "🏠 Dashboard":
        show_dashboard_home(user)
    elif page == "🔍 Nova Análise":
        show_analysis_page(user)
    elif page == "📊 Histórico":
        show_history_page(user)
    elif page == "💳 Planos":
        show_pricing_page(user)
    elif page == "⚙️ Configurações":
        show_settings_page(user)

def show_dashboard_home(user):
    """Tela inicial do dashboard."""
    st.markdown('<p class="main-header">🏠 Dashboard</p>', unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Créditos Restantes", db.get_user_credits(user['id']))
    
    with col2:
        analyses = db.get_user_analyses(user['id'], limit=1000)
        st.metric("Total de Análises", len(analyses))
    
    with col3:
        high_risk = len([a for a in analyses if a['risk_level'] in ['ALTO', 'CRÍTICO']])
        st.metric("Alertas de Alto Risco", high_risk)
    
    with col4:
        st.metric("Plano Atual", user['plan'].upper())
    
    st.markdown("---")
    
    # Últimas análises
    st.subheader("📈 Últimas Análises")
    
    recent_analyses = db.get_user_analyses(user['id'], limit=5)
    
    if recent_analyses:
        for analysis in recent_analyses:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
            
            with col1:
                st.write(f"**{analysis['type'].replace('_', ' ').title()}**")
            
            with col2:
                address_short = f"{analysis['address'][:10]}...{analysis['address'][-8:]}"
                st.write(f"`{address_short}`")
            
            with col3:
                risk_class = f"risk-{analysis['risk_level'].lower()}"
                st.markdown(f'<span class="risk-badge {risk_class}">{analysis["risk_level"]}</span>', 
                          unsafe_allow_html=True)
            
            with col4:
                date = analysis['created_at'][:10]
                st.write(f"_{date}_")
            
            st.markdown("---")
    else:
        st.info("🔍 Você ainda não fez nenhuma análise. Comece agora!")
    
    # Call to action
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Nova Análise", use_container_width=True, type="primary"):
            st.session_state.sidebar_page = "🔍 Nova Análise"
            st.rerun()
    
    with col2:
        if st.button("💳 Ver Planos", use_container_width=True):
            st.session_state.sidebar_page = "💳 Planos"
            st.rerun()

def show_analysis_page(user):
    """Página para realizar novas análises."""
    st.markdown('<p class="main-header">🔍 Nova Análise</p>', unsafe_allow_html=True)
    
    credits = db.get_user_credits(user['id'])
    
    if credits <= 0:
        st.error("❌ Você não tem créditos suficientes!")
        st.info("💡 Adquira mais créditos na página de Planos")
        if st.button("💳 Ver Planos"):
            st.session_state.sidebar_page = "💳 Planos"
            st.rerun()
        return
    
    st.info(f"💎 Você tem **{credits} créditos** disponíveis. Cada análise consome 1 crédito.")
    
    # Seleção do tipo de análise
    analysis_type = st.selectbox(
        "Tipo de Análise",
        ["🔍 Análise de Contrato Inteligente", "🕵️ Análise de Carteira (On-Chain)", "📊 Análise de Sentimento"]
    )
    
    st.markdown("---")
    
    if analysis_type == "🔍 Análise de Contrato Inteligente":
        perform_contract_analysis(user)
    elif analysis_type == "🕵️ Análise de Carteira (On-Chain)":
        perform_wallet_analysis(user)
    elif analysis_type == "📊 Análise de Sentimento":
        perform_sentiment_analysis(user)

def perform_contract_analysis(user):
    """Realiza análise de contrato."""
    st.subheader("🔍 Análise de Contrato Inteligente")
    
    contract_address = st.text_input(
        "Endereço do Contrato",
        placeholder="Ex: 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
    )
    
    network = st.selectbox("Rede", ["Ethereum", "Binance Smart Chain"])
    network_code = "eth" if network == "Ethereum" else "bsc"
    
    if st.button("🚀 Analisar Contrato", type="primary", use_container_width=True):
        if not is_valid_ethereum_address(contract_address):
            st.error("❌ Endereço de contrato inválido")
            return
        
        # Consome crédito
        if not db.use_credit(user['id']):
            st.error("❌ Créditos insuficientes")
            return
        
        with st.spinner("🤖 Analisando contrato... Isso pode levar alguns momentos."):
            try:
                result = analyze_contract(contract_address, network_code)
                
                # Salva no banco de dados
                db.save_analysis(
                    user['id'],
                    'contract_analysis',
                    contract_address,
                    result['analysis_text'],
                    result['risk_score'],
                    result['risk_level']
                )
                
                # Exibe resultado
                display_analysis_result(result, contract_address)
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")
                # Devolve o crédito em caso de erro
                db.add_credits(user['id'], 1)

def perform_wallet_analysis(user):
    """Realiza análise de carteira."""
    st.subheader("🕵️ Análise de Carteira (On-Chain)")
    
    wallet_address = st.text_input(
        "Endereço da Carteira",
        placeholder="Ex: 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
    )
    
    network = st.selectbox("Rede", ["Ethereum", "Binance Smart Chain"], key="wallet_network")
    network_code = "eth" if network == "Ethereum" else "bsc"
    
    if st.button("🚀 Analisar Carteira", type="primary", use_container_width=True):
        if not is_valid_ethereum_address(wallet_address):
            st.error("❌ Endereço de carteira inválido")
            return
        
        if not db.use_credit(user['id']):
            st.error("❌ Créditos insuficientes")
            return
        
        with st.spinner("🤖 Analisando carteira..."):
            try:
                result = analyze_wallet(wallet_address, network_code)
                
                db.save_analysis(
                    user['id'],
                    'wallet_analysis',
                    wallet_address,
                    result['analysis_text'],
                    result['risk_score'],
                    result['risk_level']
                )
                
                display_analysis_result(result, wallet_address)
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")
                db.add_credits(user['id'], 1)

def perform_sentiment_analysis(user):
    """Realiza análise de sentimento."""
    st.subheader("📊 Análise de Sentimento de Mercado")
    
    asset_ticker = st.text_input(
        "Símbolo do Ativo",
        placeholder="Ex: BTC, ETH, SOL"
    ).upper()
    
    if st.button("🚀 Analisar Sentimento", type="primary", use_container_width=True):
        if not asset_ticker:
            st.error("❌ Digite um símbolo de ativo")
            return
        
        if not db.use_credit(user['id']):
            st.error("❌ Créditos insuficientes")
            return
        
        with st.spinner(f"🤖 Analisando sentimento de {asset_ticker}..."):
            try:
                result = analyze_sentiment(asset_ticker)
                
                db.save_analysis(
                    user['id'],
                    'sentiment_analysis',
                    asset_ticker,
                    result,
                    50,  # Score neutro para sentimento
                    'MÉDIO'
                )
                
                st.success("✅ Análise concluída!")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")
                db.add_credits(user['id'], 1)

def display_analysis_result(result, address):
    """Exibe resultado da análise com formatação profissional."""
    st.success("✅ Análise concluída!")
    
    # Score de risco visual
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        risk_class = f"risk-{result['risk_level'].lower()}"
        st.markdown(
            f'<div class="risk-badge {risk_class}">Score de Risco: {result["risk_score"]}/100 - {result["risk_level"]}</div>',
            unsafe_allow_html=True
        )
    
    # Fatores de risco
    if result.get('risk_factors'):
        with st.expander("⚠️ Fatores de Risco Detectados", expanded=True):
            for factor in result['risk_factors']:
                if factor.startswith('✓'):
                    st.success(factor)
                else:
                    st.warning(factor)
    
    # Análise detalhada
    st.markdown("### 📋 Análise Detalhada")
    st.markdown(result['analysis_text'])
    
    st.markdown("---")
    st.info("💡 Esta análise foi salva no seu histórico e pode ser acessada a qualquer momento.")

def show_history_page(user):
    """Página de histórico de análises."""
    st.markdown('<p class="main-header">📊 Histórico de Análises</p>', unsafe_allow_html=True)
    
    analyses = db.get_user_analyses(user['id'], limit=100)
    
    if not analyses:
        st.info("📭 Você ainda não tem análises no histórico.")
        return
    
    st.write(f"Total de análises: **{len(analyses)}**")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        filter_type = st.selectbox(
            "Filtrar por tipo",
            ["Todos", "contract_analysis", "wallet_analysis", "sentiment_analysis"]
        )
    
    with col2:
        filter_risk = st.selectbox(
            "Filtrar por risco",
            ["Todos", "BAIXO", "MÉDIO", "ALTO", "CRÍTICO"]
        )
    
    # Aplicar filtros
    filtered = analyses
    if filter_type != "Todos":
        filtered = [a for a in filtered if a['type'] == filter_type]
    if filter_risk != "Todos":
        filtered = [a for a in filtered if a['risk_level'] == filter_risk]
    
    st.markdown("---")
    
    # Exibir análises
    for analysis in filtered:
        with st.expander(f"{analysis['type'].replace('_', ' ').title()} - {analysis['address']} ({analysis['created_at'][:10]})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Endereço:** `{analysis['address']}`")
                st.write(f"**Data:** {analysis['created_at']}")
            
            with col2:
                risk_class = f"risk-{analysis['risk_level'].lower()}"
                st.markdown(
                    f'<div class="risk-badge {risk_class}">Risco: {analysis["risk_score"]}/100 - {analysis["risk_level"]}</div>',
                    unsafe_allow_html=True
                )
            
            if st.button(f"Ver Detalhes", key=f"detail_{analysis['id']}"):
                full_analysis = db.get_analysis_by_id(analysis['id'], user['id'])
                if full_analysis:
                    st.markdown("### Análise Completa")
                    st.markdown(full_analysis['result'])

def show_pricing_page(user):
    """Página de planos e preços."""
    st.markdown('<p class="main-header">💳 Planos e Preços</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="plan-card">
            <h3>🆓 Grátis</h3>
            <h2>$0/mês</h2>
            <ul>
                <li>3 análises gratuitas</li>
                <li>Análise de contratos</li>
                <li>Análise de carteiras</li>
                <li>Score de risco automático</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if user['plan'] == 'free':
            st.success("✅ Plano Atual")
    
    with col2:
        st.markdown("""
        <div class="plan-card">
            <h3>⭐ Básico</h3>
            <h2>$49/mês</h2>
            <ul>
                <li><strong>20 análises/mês</strong></li>
                <li>Todas funcionalidades Free</li>
                <li>Análise de sentimento</li>
                <li>Histórico completo</li>
                <li>Suporte por email</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Assinar Básico", key="basic", use_container_width=True):
            # Simulação de upgrade (em produção, integrar com Stripe)
            db.upgrade_plan(user['id'], 'basic', 20)
            st.success("✅ Plano atualizado! 20 créditos adicionados.")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="plan-card">
            <h3>🚀 Pro</h3>
            <h2>$199/mês</h2>
            <ul>
                <li><strong>100 análises/mês</strong></li>
                <li>Todas funcionalidades Básico</li>
                <li>Relatórios em PDF</li>
                <li>API de acesso</li>
                <li>Suporte prioritário</li>
                <li>Alertas personalizados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Assinar Pro", key="pro", use_container_width=True):
            db.upgrade_plan(user['id'], 'pro', 100)
            st.success("✅ Plano atualizado! 100 créditos adicionados.")
            st.rerun()
    
    st.markdown("---")
    st.info("💡 **Em breve:** Integração com Stripe para pagamentos reais. Por enquanto, os upgrades são simulados para demonstração.")

def show_settings_page(user):
    """Página de configurações."""
    st.markdown('<p class="main-header">⚙️ Configurações</p>', unsafe_allow_html=True)
    
    st.subheader("👤 Informações da Conta")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Nome:** {user['full_name'] or 'Não informado'}")
    st.write(f"**Plano:** {user['plan'].upper()}")
    st.write(f"**Membro desde:** {user['created_at'][:10]}")
    
    st.markdown("---")
    
    st.subheader("🔑 API Keys")
    st.info("💡 **Em breve:** Configure suas próprias API keys (Etherscan, NewsAPI, etc.) para análises ainda mais precisas.")
    
    api_keys_status = {
        "OpenAI API": "✅ Configurada" if os.getenv("OPENAI_API_KEY") else "❌ Não configurada",
        "Etherscan API": "✅ Configurada" if os.getenv("ETHERSCAN_API_KEY") else "⚠️ Opcional (análises serão simuladas)",
        "NewsAPI": "✅ Configurada" if os.getenv("NEWSAPI_KEY") else "⚠️ Opcional (notícias serão simuladas)"
    }
    
    for api, status in api_keys_status.items():
        st.write(f"**{api}:** {status}")

# Roteamento principal
def main():
    if st.session_state.user is None:
        if st.session_state.page == 'register':
            register_page()
        else:
            login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()

