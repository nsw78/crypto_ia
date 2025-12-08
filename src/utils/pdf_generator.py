# src/utils/pdf_generator.py

from datetime import datetime
from typing import Dict
import os

class PDFGenerator:
    """
    Gerador de relatórios em PDF para análises.
    
    Nota: Esta é uma implementação simplificada que gera HTML formatado.
    Para produção, considere usar bibliotecas como:
    - reportlab
    - weasyprint
    - pdfkit
    """
    
    def __init__(self):
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_contract_report(self, analysis_data: Dict, contract_address: str, 
                                user_name: str = "") -> str:
        """
        Gera um relatório em HTML/PDF para análise de contrato.
        
        Args:
            analysis_data: Dados da análise (risk_score, risk_level, analysis_text, risk_factors)
            contract_address: Endereço do contrato analisado
            user_name: Nome do usuário que solicitou
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"contract_analysis_{contract_address[:10]}_{timestamp}.html"
        filepath = os.path.join(self.reports_dir, filename)
        
        html_content = self._generate_html_report(
            title="Análise de Contrato Inteligente",
            target=contract_address,
            analysis_data=analysis_data,
            user_name=user_name
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_wallet_report(self, analysis_data: Dict, wallet_address: str,
                              user_name: str = "") -> str:
        """Gera um relatório para análise de carteira."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wallet_analysis_{wallet_address[:10]}_{timestamp}.html"
        filepath = os.path.join(self.reports_dir, filename)
        
        html_content = self._generate_html_report(
            title="Análise de Carteira On-Chain",
            target=wallet_address,
            analysis_data=analysis_data,
            user_name=user_name
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_html_report(self, title: str, target: str, 
                             analysis_data: Dict, user_name: str) -> str:
        """Gera o HTML do relatório."""
        
        risk_score = analysis_data.get('risk_score', 0)
        risk_level = analysis_data.get('risk_level', 'N/A')
        analysis_text = analysis_data.get('analysis_text', '')
        risk_factors = analysis_data.get('risk_factors', [])
        
        # Define cor baseada no nível de risco
        risk_colors = {
            'BAIXO': '#10b981',
            'MÉDIO': '#f59e0b',
            'ALTO': '#ef4444',
            'CRÍTICO': '#7f1d1d'
        }
        risk_color = risk_colors.get(risk_level, '#6b7280')
        
        # Formata fatores de risco
        factors_html = ""
        for factor in risk_factors:
            icon = "✅" if factor.startswith('✓') else "⚠️"
            color = "#10b981" if factor.startswith('✓') else "#f59e0b"
            factors_html += f'<li style="color: {color}; margin: 0.5rem 0;">{icon} {factor}</li>'
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Crypto IA Auditor</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f9fafb;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 2rem;
        }}
        
        .info-section {{
            background: #f3f4f6;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
        }}
        
        .info-label {{
            font-weight: 600;
            color: #6b7280;
        }}
        
        .info-value {{
            color: #1f2937;
        }}
        
        .risk-badge {{
            display: inline-block;
            background: {risk_color};
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 2rem 0;
            text-align: center;
            width: 100%;
        }}
        
        .section-title {{
            font-size: 1.8rem;
            color: #1f2937;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }}
        
        .factors-list {{
            list-style: none;
            padding: 1rem;
            background: #f9fafb;
            border-radius: 10px;
        }}
        
        .analysis-text {{
            background: #f9fafb;
            padding: 2rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            white-space: pre-wrap;
            line-height: 1.8;
        }}
        
        .footer {{
            background: #f3f4f6;
            padding: 2rem;
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
        }}
        
        .disclaimer {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            margin: 2rem 0;
            border-radius: 5px;
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Crypto IA Auditor</h1>
            <p>{title}</p>
        </div>
        
        <div class="content">
            <div class="info-section">
                <h2 style="margin-bottom: 1rem; color: #1f2937;">Informações do Relatório</h2>
                <div class="info-row">
                    <span class="info-label">Data da Análise:</span>
                    <span class="info-value">{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Endereço Analisado:</span>
                    <span class="info-value" style="font-family: monospace;">{target}</span>
                </div>
                {f'<div class="info-row"><span class="info-label">Solicitado por:</span><span class="info-value">{user_name}</span></div>' if user_name else ''}
                <div class="info-row">
                    <span class="info-label">Powered by:</span>
                    <span class="info-value">OpenAI GPT-4 + Análise Automatizada</span>
                </div>
            </div>
            
            <div style="text-align: center;">
                <div class="risk-badge">
                    Score de Risco: {risk_score}/100 - {risk_level}
                </div>
            </div>
            
            {f'''
            <h2 class="section-title">⚠️ Fatores de Risco Detectados</h2>
            <ul class="factors-list">
                {factors_html}
            </ul>
            ''' if risk_factors else ''}
            
            <h2 class="section-title">📋 Análise Detalhada</h2>
            <div class="analysis-text">
{analysis_text}
            </div>
            
            <div class="disclaimer">
                <strong>⚠️ Disclaimer:</strong> Esta análise é gerada automaticamente por IA e não constitui 
                aconselhamento financeiro. Sempre faça sua própria pesquisa (DYOR) antes de investir em 
                qualquer ativo. A precisão das análises depende da qualidade dos dados disponíveis.
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Crypto IA Auditor</strong> - Auditoria Inteligente de Contratos</p>
            <p>© 2025 Todos os direitos reservados</p>
            <p style="margin-top: 1rem; font-size: 0.8rem;">
                Este relatório é confidencial e destinado exclusivamente ao uso do solicitante.
            </p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def convert_html_to_pdf(self, html_path: str) -> str:
        """
        Converte HTML para PDF (requer biblioteca externa).
        
        Para implementar em produção, instale uma das bibliotecas:
        
        pip install weasyprint
        ou
        pip install pdfkit wkhtmltopdf
        
        Exemplo com weasyprint:
        from weasyprint import HTML
        pdf_path = html_path.replace('.html', '.pdf')
        HTML(html_path).write_pdf(pdf_path)
        return pdf_path
        """
        # Por enquanto, retorna o caminho do HTML
        # Em produção, implementar conversão real
        return html_path

# Instância global
pdf_generator = PDFGenerator()

