# src/payment/stripe_integration.py

"""
Integração com Stripe para pagamentos.

Para usar em produção:
1. Instale: pip install stripe
2. Configure suas chaves no .env:
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLIC_KEY=pk_test_...
3. Crie produtos e preços no Dashboard do Stripe
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class StripePaymentHandler:
    """Gerencia pagamentos via Stripe."""
    
    def __init__(self):
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "")
        self.stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY", "")
        
        # IDs dos produtos no Stripe (configurar no dashboard)
        self.PLANS = {
            'basic': {
                'name': 'Plano Básico',
                'price': 49.00,
                'credits': 20,
                'stripe_price_id': 'price_basic_monthly',  # Substituir pelo ID real
            },
            'pro': {
                'name': 'Plano Pro',
                'price': 199.00,
                'credits': 100,
                'stripe_price_id': 'price_pro_monthly',  # Substituir pelo ID real
            }
        }
    
    def create_checkout_session(self, plan: str, user_email: str, 
                               success_url: str, cancel_url: str) -> Optional[Dict]:
        """
        Cria uma sessão de checkout no Stripe.
        
        Args:
            plan: 'basic' ou 'pro'
            user_email: Email do usuário
            success_url: URL de redirecionamento após sucesso
            cancel_url: URL de redirecionamento se cancelar
            
        Returns:
            Dict com session_id e url do checkout ou None
        """
        if not self.stripe_secret_key:
            return self._simulate_checkout(plan, user_email)
        
        try:
            import stripe
            stripe.api_key = self.stripe_secret_key
            
            plan_info = self.PLANS.get(plan)
            if not plan_info:
                return None
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan_info['stripe_price_id'],
                    'quantity': 1,
                }],
                mode='subscription',
                customer_email=user_email,
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={
                    'plan': plan,
                    'credits': plan_info['credits']
                }
            )
            
            return {
                'session_id': session.id,
                'url': session.url
            }
            
        except Exception as e:
            print(f"Erro ao criar sessão de checkout: {e}")
            return None
    
    def create_payment_link(self, plan: str) -> Optional[str]:
        """
        Cria um link de pagamento para um plano.
        
        Returns:
            URL do link de pagamento ou None
        """
        if not self.stripe_secret_key:
            return self._simulate_payment_link(plan)
        
        try:
            import stripe
            stripe.api_key = self.stripe_secret_key
            
            plan_info = self.PLANS.get(plan)
            if not plan_info:
                return None
            
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    'price': plan_info['stripe_price_id'],
                    'quantity': 1
                }],
            )
            
            return payment_link.url
            
        except Exception as e:
            print(f"Erro ao criar link de pagamento: {e}")
            return None
    
    def verify_payment(self, session_id: str) -> Optional[Dict]:
        """
        Verifica se um pagamento foi concluído.
        
        Returns:
            Dict com informações do pagamento ou None
        """
        if not self.stripe_secret_key:
            return self._simulate_payment_verification(session_id)
        
        try:
            import stripe
            stripe.api_key = self.stripe_secret_key
            
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                return {
                    'status': 'paid',
                    'amount': session.amount_total / 100,  # Converte de centavos
                    'currency': session.currency,
                    'customer_email': session.customer_email,
                    'plan': session.metadata.get('plan'),
                    'credits': int(session.metadata.get('credits', 0))
                }
            
            return None
            
        except Exception as e:
            print(f"Erro ao verificar pagamento: {e}")
            return None
    
    def create_customer_portal_session(self, customer_id: str, 
                                      return_url: str) -> Optional[str]:
        """
        Cria uma sessão do portal do cliente para gerenciar assinaturas.
        
        Returns:
            URL do portal ou None
        """
        if not self.stripe_secret_key:
            return None
        
        try:
            import stripe
            stripe.api_key = self.stripe_secret_key
            
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            return session.url
            
        except Exception as e:
            print(f"Erro ao criar portal do cliente: {e}")
            return None
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancela uma assinatura."""
        if not self.stripe_secret_key:
            return True  # Simula sucesso
        
        try:
            import stripe
            stripe.api_key = self.stripe_secret_key
            
            stripe.Subscription.delete(subscription_id)
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar assinatura: {e}")
            return False
    
    # Métodos de simulação (para desenvolvimento sem Stripe configurado)
    
    def _simulate_checkout(self, plan: str, user_email: str) -> Dict:
        """Simula criação de checkout para desenvolvimento."""
        return {
            'session_id': f'sim_session_{plan}_{user_email}',
            'url': 'https://checkout.stripe.com/simulated',
            'simulated': True
        }
    
    def _simulate_payment_link(self, plan: str) -> str:
        """Simula link de pagamento."""
        return f'https://buy.stripe.com/simulated_{plan}'
    
    def _simulate_payment_verification(self, session_id: str) -> Dict:
        """Simula verificação de pagamento."""
        # Extrai plano do session_id simulado
        plan = 'basic' if 'basic' in session_id else 'pro'
        plan_info = self.PLANS[plan]
        
        return {
            'status': 'paid',
            'amount': plan_info['price'],
            'currency': 'usd',
            'customer_email': 'simulated@example.com',
            'plan': plan,
            'credits': plan_info['credits'],
            'simulated': True
        }

# Instância global
stripe_handler = StripePaymentHandler()

# Exemplo de uso (webhook handler)
def handle_stripe_webhook(payload: str, sig_header: str) -> bool:
    """
    Handler para webhooks do Stripe.
    
    Configure no Dashboard do Stripe:
    https://dashboard.stripe.com/webhooks
    
    Eventos importantes:
    - checkout.session.completed
    - customer.subscription.created
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    if not os.getenv("STRIPE_WEBHOOK_SECRET"):
        return False
    
    try:
        import stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        
        # Processa diferentes tipos de eventos
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Atualizar banco de dados: adicionar créditos ao usuário
            print(f"Pagamento concluído: {session.get('customer_email')}")
            
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            # Rebaixar plano do usuário para free
            print(f"Assinatura cancelada: {subscription.get('customer')}")
        
        return True
        
    except Exception as e:
        print(f"Erro no webhook: {e}")
        return False

