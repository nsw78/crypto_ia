# app.py

import streamlit as st
from src.analysis.contract_analyzer import analyze_contract
from src.analysis.onchain_analyzer import analyze_wallet
from src.analysis.sentiment_analyzer import analyze_sentiment
from src.utils.helpers import is_valid_ethereum_address

# --- Configuração da Página ---
st.set_page_config(
    page_title="Crypto IA Tools",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Barra Lateral (Sidebar) ---
st.sidebar.title("Crypto IA Tools 🤖")
st.sidebar.markdown("Uma suíte de ferramentas com IA para análise de blockchain e criptomoedas.")
st.sidebar.markdown("---")

# Seleção da ferramenta
tool_selection = st.sidebar.selectbox(
    "Selecione a ferramenta:",
    ["Análise de Contrato Inteligente", "Análise de Carteira (On-Chain)", "Análise de Sentimento de Mercado"]
)
st.sidebar.markdown("---")
st.sidebar.info("Este é um protótipo. As análises são geradas por IA e não constituem aconselhamento financeiro.")


# --- Corpo Principal da Aplicação ---

if tool_selection == "Análise de Contrato Inteligente":
    st.title("🔍 Análise de Contrato Inteligente")
    st.markdown("Cole o endereço de um contrato inteligente (ex: Ethereum, BSC) para que a IA procure por riscos, vulnerabilidades e potenciais `rug pulls`.")

    contract_address = st.text_input("Endereço do Contrato:", placeholder="Ex: 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")

    if st.button("Analisar Contrato"):
        if is_valid_ethereum_address(contract_address):
            with st.spinner("A IA está analisando o contrato... Isso pode levar um momento."):
                try:
                    analysis_result = analyze_contract(contract_address)
                    st.subheader("Resultados da Análise:")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}. Verifique se sua chave de API da OpenAI está configurada corretamente em um arquivo `.env`.")
        else:
            st.error("Por favor, insira um endereço de contrato válido (começando com 0x).")

elif tool_selection == "Análise de Carteira (On-Chain)":
    st.title("🕵️ Análise de Carteira (On-Chain)")
    st.markdown("Insira o endereço de uma carteira para que a IA analise o histórico de transações em busca de padrões suspeitos.")

    wallet_address = st.text_input("Endereço da Carteira:", placeholder="Ex: 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae")

    if st.button("Analisar Carteira"):
        if is_valid_ethereum_address(wallet_address):
            with st.spinner("A IA está vasculhando a blockchain..."):
                try:
                    analysis_result = analyze_wallet(wallet_address)
                    st.subheader("Resultados da Análise:")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}. Verifique sua chave de API.")
        else:
            st.error("Por favor, insira um endereço de carteira válido (começando com 0x).")

elif tool_selection == "Análise de Sentimento de Mercado":
    st.title("📊 Análise de Sentimento de Mercado")
    st.markdown("Digite o símbolo de um ativo (ex: BTC, ETH) para que a IA analise as últimas notícias e o sentimento das redes sociais.")

    asset_ticker = st.text_input("Símbolo do Ativo:", placeholder="Ex: BTC, ETH, SOL").upper()

    if st.button("Analisar Sentimento"):
        if asset_ticker:
            with st.spinner(f"A IA está lendo as notícias sobre {asset_ticker}..."):
                try:
                    analysis_result = analyze_sentiment(asset_ticker)
                    st.subheader(f"Resultados da Análise para {asset_ticker}:")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}. Verifique sua chave de API.")
        else:
            st.error("Por favor, insira um símbolo de ativo.")

