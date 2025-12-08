# src/database/db_manager.py

import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class DatabaseManager:
    """Gerencia o banco de dados SQLite para usuários, créditos e análises."""
    
    def __init__(self, db_path: str = "crypto_ia.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Cria uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                plan TEXT DEFAULT 'free',
                credits INTEGER DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                stripe_customer_id TEXT
            )
        ''')
        
        # Tabela de análises
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analysis_type TEXT NOT NULL,
                target_address TEXT NOT NULL,
                result TEXT,
                risk_score INTEGER,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabela de transações (pagamentos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                plan TEXT NOT NULL,
                credits_added INTEGER NOT NULL,
                stripe_payment_id TEXT,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabela de API keys (para futura API pública)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                name TEXT,
                is_active BOOLEAN DEFAULT 1,
                requests_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash SHA-256 da senha."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email: str, password: str, full_name: str = "") -> Optional[int]:
        """
        Cria um novo usuário.
        
        Returns:
            ID do usuário criado ou None se o email já existir.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, credits)
                VALUES (?, ?, ?, 3)
            ''', (email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário.
        
        Returns:
            Dicionário com dados do usuário ou None se falhar.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, email, full_name, plan, credits, created_at
            FROM users
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        result = cursor.fetchone()
        
        if result:
            # Atualiza último login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (result[0],))
            conn.commit()
            
            user_data = {
                'id': result[0],
                'email': result[1],
                'full_name': result[2],
                'plan': result[3],
                'credits': result[4],
                'created_at': result[5]
            }
            conn.close()
            return user_data
        
        conn.close()
        return None
    
    def get_user_credits(self, user_id: int) -> int:
        """Retorna o número de créditos do usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT credits FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 0
    
    def use_credit(self, user_id: int) -> bool:
        """
        Consome um crédito do usuário.
        
        Returns:
            True se bem-sucedido, False se sem créditos.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT credits FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            cursor.execute('''
                UPDATE users SET credits = credits - 1
                WHERE id = ?
            ''', (user_id,))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def add_credits(self, user_id: int, amount: int):
        """Adiciona créditos ao usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET credits = credits + ?
            WHERE id = ?
        ''', (amount, user_id))
        
        conn.commit()
        conn.close()
    
    def upgrade_plan(self, user_id: int, plan: str, credits: int):
        """Faz upgrade do plano do usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET plan = ?, credits = credits + ?
            WHERE id = ?
        ''', (plan, credits, user_id))
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, user_id: int, analysis_type: str, target_address: str, 
                     result: str, risk_score: int, risk_level: str) -> int:
        """
        Salva uma análise no banco de dados.
        
        Returns:
            ID da análise criada.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analyses (user_id, analysis_type, target_address, result, risk_score, risk_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, analysis_type, target_address, result, risk_score, risk_level))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    
    def get_user_analyses(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Retorna o histórico de análises do usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, analysis_type, target_address, risk_score, risk_level, created_at
            FROM analyses
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in results:
            analyses.append({
                'id': row[0],
                'type': row[1],
                'address': row[2],
                'risk_score': row[3],
                'risk_level': row[4],
                'created_at': row[5]
            })
        
        return analyses
    
    def get_analysis_by_id(self, analysis_id: int, user_id: int) -> Optional[Dict]:
        """Retorna uma análise específica."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, analysis_type, target_address, result, risk_score, risk_level, created_at
            FROM analyses
            WHERE id = ? AND user_id = ?
        ''', (analysis_id, user_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'type': result[1],
                'address': result[2],
                'result': result[3],
                'risk_score': result[4],
                'risk_level': result[5],
                'created_at': result[6]
            }
        
        return None
    
    def record_transaction(self, user_id: int, amount: float, plan: str, 
                          credits_added: int, stripe_payment_id: str = None) -> int:
        """Registra uma transação de pagamento."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, plan, credits_added, stripe_payment_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, plan, credits_added, stripe_payment_id))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return transaction_id
    
    def get_user_transactions(self, user_id: int) -> List[Dict]:
        """Retorna o histórico de transações do usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, amount, currency, plan, credits_added, status, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        transactions = []
        for row in results:
            transactions.append({
                'id': row[0],
                'amount': row[1],
                'currency': row[2],
                'plan': row[3],
                'credits_added': row[4],
                'status': row[5],
                'created_at': row[6]
            })
        
        return transactions

# Instância global
db = DatabaseManager()

