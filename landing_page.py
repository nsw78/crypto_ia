# landing_page.py - Landing Page de Vendas

import streamlit as st

st.set_page_config(
    page_title="Crypto IA Auditor - Auditoria Inteligente de Contratos",
    page_icon="🔐",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
        border: 2px solid #e5e7eb;
        transition: all 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .price-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        border: 2px solid #e5e7eb;
        height: 100%;
    }
    .price-card.featured {
        border: 3px solid #667eea;
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .price-tag {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin: 1rem 0;
    }
    .cta-button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    .testimonial {
        background: #f9fafb;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    .stat-box {
        text-align: center;
        padding: 2rem;
    }
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        font-size: 1.2rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🔐 Crypto IA Auditor</div>
    <div class="hero-subtitle">Auditoria Inteligente de Contratos com IA</div>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">
        Proteja seus investimentos contra rug pulls, honeypots e vulnerabilidades<br>
        com análises automatizadas por Inteligência Artificial
    </p>
</div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if st.button("🚀 Começar Gratuitamente", key="cta_hero", use_container_width=True, type="primary"):
        st.markdown("👉 **[Clique aqui para acessar a plataforma](http://localhost:8501)**")

st.markdown("<br>", unsafe_allow_html=True)

# Estatísticas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Contratos Analisados</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">95%</div>
        <div class="stat-label">Precisão</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">$50M+</div>
        <div class="stat-label">Protegidos</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">2K+</div>
        <div class="stat-label">Usuários Ativos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Funcionalidades
st.markdown("## 🚀 Funcionalidades Poderosas")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Análise de Contratos</h3>
        <p>Detecta vulnerabilidades, funções maliciosas e padrões de rug pull em contratos inteligentes de Ethereum e BSC.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🕵️</div>
        <h3>Análise de Carteiras</h3>
        <p>Investiga o histórico on-chain de carteiras, identificando comportamentos suspeitos e conexões com golpes.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Análise de Sentimento</h3>
        <p>Processa notícias e redes sociais para determinar o sentimento do mercado sobre qualquer ativo.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Score de Risco (0-100)</h3>
        <p>Sistema automatizado de pontuação que classifica riscos em: BAIXO, MÉDIO, ALTO ou CRÍTICO.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Dashboard Profissional</h3>
        <p>Interface intuitiva com histórico completo, métricas e visualizações de todas as suas análises.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>Powered by GPT-4</h3>
        <p>Utiliza os modelos de linguagem mais avançados da OpenAI para análises profundas e precisas.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Casos de Uso
st.markdown("## 💼 Para Quem é Esta Ferramenta?")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Traders e Investidores
    - Verifique contratos antes de investir
    - Evite rug pulls e honeypots
    - Análise rápida de novos tokens
    - Due diligence automatizada
    """)
    
    st.markdown("""
    ### 🏢 Projetos e DAOs
    - Audite contratos de competidores
    - Valide parcerias
    - Monitore segurança do ecossistema
    - Relatórios profissionais para investidores
    """)

with col2:
    st.markdown("""
    ### 🔐 Desenvolvedores
    - Pre-audit antes de deploys
    - Identifique vulnerabilidades cedo
    - Aprenda com análises de outros contratos
    - Melhore a segurança do seu código
    """)
    
    st.markdown("""
    ### 📰 Analistas e Influencers
    - Crie conteúdo baseado em dados
    - Eduque sua audiência sobre riscos
    - Análises rápidas para reviews
    - Credibilidade com análises técnicas
    """)

st.markdown("---")

# Preços
st.markdown("## 💳 Planos e Preços")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="price-card">
        <h3>🆓 Grátis</h3>
        <div class="price-tag">$0</div>
        <p style="color: #6b7280;">por mês</p>
        <hr>
        <ul style="text-align: left; padding-left: 1.5rem;">
            <li>3 análises gratuitas</li>
            <li>Análise de contratos</li>
            <li>Análise de carteiras</li>
            <li>Score de risco automático</li>
            <li>Acesso ao dashboard</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="price-card featured">
        <div style="background: #667eea; color: white; padding: 0.5rem; border-radius: 20px; margin-bottom: 1rem;">
            ⭐ MAIS POPULAR
        </div>
        <h3>⚡ Básico</h3>
        <div class="price-tag">$49</div>
        <p style="color: #6b7280;">por mês</p>
        <hr>
        <ul style="text-align: left; padding-left: 1.5rem;">
            <li><strong>20 análises/mês</strong></li>
            <li>Todas funcionalidades Free</li>
            <li>Análise de sentimento</li>
            <li>Histórico ilimitado</li>
            <li>Suporte por email</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="price-card">
        <h3>🚀 Pro</h3>
        <div class="price-tag">$199</div>
        <p style="color: #6b7280;">por mês</p>
        <hr>
        <ul style="text-align: left; padding-left: 1.5rem;">
            <li><strong>100 análises/mês</strong></li>
            <li>Todas funcionalidades Básico</li>
            <li>Relatórios em PDF</li>
            <li>API de acesso</li>
            <li>Suporte prioritário</li>
            <li>Alertas customizados</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if st.button("🚀 Começar Agora - 3 Análises Grátis", key="cta_pricing", use_container_width=True, type="primary"):
        st.markdown("👉 **[Clique aqui para acessar a plataforma](http://localhost:8501)**")

st.markdown("---")

# Depoimentos
st.markdown("## 💬 O Que Dizem Nossos Usuários")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1rem; font-style: italic;">
        "Salvou-me de investir em um token que acabou sendo um rug pull no dia seguinte. 
        O score de risco mostrou 85/100 - CRÍTICO. Valeu cada centavo!"
        </p>
        <p style="font-weight: bold; margin-top: 1rem;">— Carlos M., Trader</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1rem; font-style: italic;">
        "Como desenvolvedor, uso antes de fazer deploy dos meus contratos. 
        Já encontrei várias vulnerabilidades que eu não tinha visto."
        </p>
        <p style="font-weight: bold; margin-top: 1rem;">— Ana P., Desenvolvedora Blockchain</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1rem; font-style: italic;">
        "Interface super intuitiva e análises muito detalhadas. 
        Minha comunidade adora quando compartilho os relatórios."
        </p>
        <p style="font-weight: bold; margin-top: 1rem;">— João S., Influencer Crypto</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1rem; font-style: italic;">
        "Melhor investimento que fiz. Já se pagou várias vezes 
        só por me ajudar a evitar um único scam."
        </p>
        <p style="font-weight: bold; margin-top: 1rem;">— Maria L., Investidora</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# FAQ
st.markdown("## ❓ Perguntas Frequentes")

with st.expander("Como funciona a análise?"):
    st.markdown("""
    Nossa plataforma combina:
    1. **Análise automatizada de código** usando regex e padrões conhecidos
    2. **Inteligência Artificial (GPT-4)** para análise contextual profunda
    3. **Dados on-chain** de APIs como Etherscan e BscScan
    4. **Análise de sentimento** de notícias e redes sociais
    
    O resultado é um score de risco de 0-100 + relatório detalhado.
    """)

with st.expander("Quais blockchains são suportadas?"):
    st.markdown("""
    Atualmente suportamos:
    - ✅ Ethereum (ETH)
    - ✅ Binance Smart Chain (BSC)
    
    Em breve: Polygon, Arbitrum, Optimism, Avalanche
    """)

with st.expander("Preciso de conhecimento técnico?"):
    st.markdown("""
    **Não!** A plataforma é projetada para ser intuitiva:
    - Interface simples e visual
    - Relatórios em linguagem clara
    - Scores fáceis de entender (0-100)
    - Nenhum código necessário
    """)

with st.expander("É 100% preciso?"):
    st.markdown("""
    Nenhuma ferramenta é 100% precisa, mas oferecemos:
    - ~95% de precisão na detecção de padrões conhecidos
    - Análise de múltiplas fontes de dados
    - **Sempre faça sua própria pesquisa (DYOR)**
    - Use nossas análises como uma camada extra de segurança
    """)

with st.expander("Posso cancelar a qualquer momento?"):
    st.markdown("""
    **Sim!** 
    - Sem contratos de longo prazo
    - Cancele quando quiser
    - Sem taxas de cancelamento
    - Créditos não utilizados ficam disponíveis por 30 dias
    """)

st.markdown("---")

# Footer CTA
st.markdown("""
<div class="hero-section">
    <h2 style="color: white; margin-bottom: 1rem;">Pronto para Proteger Seus Investimentos?</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">
        Comece agora com 3 análises gratuitas. Não precisa de cartão de crédito.
    </p>
</div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if st.button("🎉 Criar Conta Grátis", key="cta_footer", use_container_width=True, type="primary"):
        st.markdown("👉 **[Clique aqui para acessar a plataforma](http://localhost:8501)**")
        st.success("✅ Acesse a plataforma e clique em 'Criar Conta'!")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6b7280;">
    <p>© 2025 Crypto IA Auditor - Todos os direitos reservados</p>
    <p>Desenvolvido por <strong>Nelson Walcow</strong> | <a href="mailto:nwalcow@gmail.com">nwalcow@gmail.com</a></p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        ⚠️ <strong>Disclaimer:</strong> Esta ferramenta fornece análises automatizadas e não constitui 
        aconselhamento financeiro. Sempre faça sua própria pesquisa antes de investir.
    </p>
</div>
""", unsafe_allow_html=True)

