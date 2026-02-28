<p align="center">
  <img src="api/static/favicon.svg" alt="Crypto IA Auditor" width="120" height="120">
</p>

<h1 align="center">Crypto IA Auditor</h1>

<p align="center">
  <strong>Enterprise-grade API for intelligent smart contract auditing, wallet forensics & market sentiment analysis</strong>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/version-3.0.0-blue.svg" alt="Version 3.0.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white" alt="Python 3.12+"></a>
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker Ready"></a>
  <a href="#"><img src="https://img.shields.io/badge/tests-22%20passed-brightgreen.svg" alt="Tests 22 passed"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#api-reference">API Reference</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#deployment">Deployment</a> &bull;
  <a href="#testing">Testing</a>
</p>

---

## Overview

**Crypto IA Auditor** is a production-ready SaaS platform that combines AI-powered analysis with real blockchain data to protect crypto investors from rug pulls, honeypots, and smart contract vulnerabilities.

| Capability | Description |
|---|---|
| **Smart Contract Audit** | Automated vulnerability detection, pattern analysis, and risk scoring for EVM contracts |
| **Wallet Forensics** | On-chain behavioral analysis, mixer detection, and transaction history profiling |
| **Market Sentiment** | Real-time news aggregation and AI-powered sentiment classification |
| **Risk Scoring** | Automated 0-100 risk score with multi-factor analysis engine |

**Author:** Nelson Walcow — nwalcow@gmail.com

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/crypto-ia-auditor.git
cd crypto-ia-auditor

# Configure environment
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY

# Build and start all services
docker compose up -d --build

# Verify
curl http://localhost:8085/api/v1/health
```

| Service | URL | Description |
|---|---|---|
| **REST API** | `http://localhost:8085` | FastAPI + Swagger docs at `/docs` |
| **Frontend** | `http://localhost:8503` | Streamlit SaaS dashboard |
| **Landing Page** | `http://localhost:8504` | Marketing / sales page |
| **Redis** | `localhost:6385` | Cache & rate limiting backend |

### Option 2: Local Development

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-api.txt

# Configure environment
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY

# Run the API server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run the Streamlit frontend (separate terminal)
streamlit run app_saas.py
```

---

## API Reference

Base URL: `/api/v1`

### Authentication

All protected endpoints require either:
- **JWT Bearer Token**: `Authorization: Bearer <token>`
- **API Key**: `X-API-Key: <key>`

### Endpoints

#### Health

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/health` | Service health check | No |
| `GET` | `/health/ready` | Readiness probe (DB connectivity) | No |

#### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Create new account | No |
| `POST` | `/auth/login` | Obtain JWT tokens | No |
| `POST` | `/auth/refresh` | Refresh access token | Bearer |

#### Analysis

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/analysis/contract` | Audit a smart contract | Bearer / API Key |
| `POST` | `/analysis/wallet` | Analyze a wallet address | Bearer / API Key |
| `POST` | `/analysis/sentiment` | Run sentiment analysis | Bearer / API Key |
| `GET` | `/analysis/history` | List past analyses (paginated) | Bearer / API Key |
| `GET` | `/analysis/{id}` | Get specific analysis result | Bearer / API Key |

#### Market Data

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/market/price/{coin_id}` | Get coin price data | Bearer / API Key |
| `GET` | `/market/trending` | Trending cryptocurrencies | Bearer / API Key |

#### User Management

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/user/me` | Get user profile | Bearer |
| `GET` | `/user/credits` | Check remaining credits | Bearer |
| `POST` | `/user/purchase` | Purchase a plan | Bearer |
| `GET` | `/user/api-keys` | List API keys | Bearer |
| `POST` | `/user/api-keys` | Generate new API key | Bearer |
| `DELETE` | `/user/api-keys/{id}` | Revoke an API key | Bearer |

#### Webhooks

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/webhooks/stripe` | Stripe payment webhook | Signature |

### Example: Register + Analyze

```bash
# 1. Register
curl -X POST http://localhost:8085/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123", "full_name": "John Doe"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8085/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123"}' | jq -r '.access_token')

# 3. Analyze a smart contract
curl -X POST http://localhost:8085/api/v1/analysis/contract \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "network": "eth"}'
```

Interactive docs available at **http://localhost:8085/docs** (Swagger UI) and **http://localhost:8085/redoc** (ReDoc).

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTS                              │
│   Browser / cURL / SDK / Streamlit Frontend              │
└───────────────┬─────────────────────────────────────────┘
                │ HTTPS
┌───────────────▼─────────────────────────────────────────┐
│                   FastAPI (api/main.py)                   │
│  ┌──────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │   CORS   │ │ Rate Limiter │ │  Request Logging     │ │
│  │ GZip     │ │  60 req/min  │ │  X-Request-ID        │ │
│  └──────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Error Handler Middleware               │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│                     ROUTES (/api/v1)                      │
│  /auth  /analysis  /market  /user  /health  /webhooks    │
├──────────────────────────────────────────────────────────┤
│                    DEPENDENCIES                           │
│  JWT Auth │ API Key Auth │ Credit Check │ DB Session     │
├──────────────────────────────────────────────────────────┤
│                     SERVICES                              │
│  AnalysisService (async) │ PaymentService                │
├────────────┬────────────┬────────────┬───────────────────┤
│  Analysis  │ Connectors │    LLM     │    Database       │
│  ─contract │ ─etherscan │ ─gpt-4    │ ─SQLAlchemy async │
│  ─wallet   │ ─coingecko │ ─prompts  │ ─SQLite/Postgres  │
│  ─sentiment│ ─newsapi   │           │ ─CRUD ops         │
│  ─risk     │ ─blockchain│           │                   │
├────────────┴────────────┴────────────┴───────────────────┤
│                  INFRASTRUCTURE                           │
│  Docker Compose │ Redis (cache) │ Stripe (payments)      │
└──────────────────────────────────────────────────────────┘
```

### Project Structure

```
crypto_ia/
├── api/                        # Enterprise REST API
│   ├── main.py                 # FastAPI application entrypoint
│   ├── core/
│   │   ├── config.py           # Pydantic settings management
│   │   ├── security.py         # JWT + bcrypt + API key auth
│   │   ├── exceptions.py       # Error hierarchy
│   │   ├── logging.py          # Structured logging (structlog)
│   │   └── deps.py             # Dependency injection
│   ├── database/
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   ├── session.py          # Async engine & session factory
│   │   └── crud.py             # Data access layer
│   ├── schemas/
│   │   ├── auth.py             # Auth request/response models
│   │   ├── analysis.py         # Analysis schemas
│   │   └── common.py           # Shared schemas
│   ├── services/
│   │   ├── analysis_service.py # Async analysis orchestrator
│   │   └── payment_service.py  # Plan purchase logic
│   ├── routes/
│   │   ├── auth.py             # /auth endpoints
│   │   ├── analysis.py         # /analysis endpoints
│   │   ├── market.py           # /market endpoints
│   │   ├── user.py             # /user endpoints
│   │   ├── health.py           # /health endpoints
│   │   └── webhooks.py         # Stripe webhook handler
│   ├── middleware/
│   │   ├── rate_limiter.py     # In-memory rate limiting
│   │   ├── request_logging.py  # Request ID + timing
│   │   └── error_handler.py    # Global exception handler
│   └── static/
│       ├── favicon.ico         # Multi-size ICO (16-256px)
│       ├── favicon.png         # 256px PNG
│       └── favicon.svg         # Vector favicon
├── src/                        # Core analysis engine
│   ├── analysis/
│   │   ├── contract_analyzer.py
│   │   ├── onchain_analyzer.py
│   │   ├── sentiment_analyzer.py
│   │   └── risk_scoring.py
│   ├── connectors/
│   │   ├── etherscan_api.py
│   │   ├── coingecko_api.py
│   │   ├── news_api.py
│   │   └── blockchain_api.py
│   ├── database/
│   │   └── db_manager.py
│   ├── llm/
│   │   ├── llm_client.py
│   │   └── prompts.py
│   ├── payment/
│   │   └── stripe_integration.py
│   └── utils/
│       ├── helpers.py
│       └── pdf_generator.py
├── tests/                      # Automated test suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_user.py
│   ├── test_health.py
│   └── test_analysis.py
├── app_saas.py                 # Streamlit SaaS frontend
├── landing_page.py             # Streamlit landing page
├── Dockerfile                  # Multi-service container
├── docker-compose.yml          # Full stack orchestration
├── requirements-api.txt        # API dependencies
├── requirements.txt            # Frontend dependencies
├── pytest.ini                  # Test configuration
├── .env.example                # Environment template
└── README.md
```

---

## Security

| Layer | Implementation |
|---|---|
| **Authentication** | JWT (HS256) with access + refresh tokens, bcrypt password hashing (12 rounds) |
| **API Keys** | SHA-256 hashed keys with per-key usage tracking and revocation |
| **Rate Limiting** | 60 req/min per IP with `X-RateLimit-*` response headers |
| **Input Validation** | Pydantic v2 schemas with regex-validated Ethereum addresses |
| **Error Handling** | Sanitized error responses — no stack traces in production |
| **CORS** | Configurable allowed origins |
| **Request Tracing** | Unique `X-Request-ID` per request, `X-Response-Time` header |
| **Structured Logging** | JSON-formatted logs via structlog with request context |
| **Non-root Container** | Docker runs as `appuser`, not root |

---

## Risk Scoring Engine

Automated multi-factor scoring system (0-100):

| Score Range | Level | Indicator |
|---|---|---|
| 0 – 20 | **LOW** | Safe — verified contracts, standard patterns |
| 21 – 45 | **MEDIUM** | Caution — some privileged functions detected |
| 46 – 70 | **HIGH** | Warning — suspicious patterns (onlyOwner, withdraw) |
| 71 – 100 | **CRITICAL** | Danger — honeypot/rug pull patterns detected |

**Factors analyzed:** `selfdestruct`, `delegatecall`, privileged functions, honeypot patterns, rug pull indicators, code complexity, OpenZeppelin usage, wallet behavior patterns.

---

## Configuration

All configuration is done via environment variables. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | **Yes** | — | JWT signing key (`openssl rand -hex 32`) |
| `OPENAI_API_KEY` | **Yes** | — | OpenAI API key for GPT-4 analysis |
| `DATABASE_URL` | No | `sqlite+aiosqlite:///./crypto_ia.db` | Async database URL |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis for caching |
| `ETHERSCAN_API_KEY` | No | — | Etherscan API (uses sample data without) |
| `NEWSAPI_KEY` | No | — | NewsAPI for sentiment (uses simulated without) |
| `STRIPE_SECRET_KEY` | No | — | Stripe payments (simulated without) |
| `RATE_LIMIT_PER_MINUTE` | No | `60` | Max requests per minute per IP |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `LOG_FORMAT` | No | `json` | Log format (`json` or `console`) |

---

## Deployment

### Docker Compose (Production)

```bash
# Build all services
docker compose build

# Start in detached mode
docker compose up -d

# View logs
docker compose logs -f api

# Stop
docker compose down
```

**Services launched:**

| Container | Image | Internal Port | External Port |
|---|---|---|---|
| `crypto-ia-api` | Custom (Python 3.12) | 8000 | 8085 |
| `crypto-ia-frontend` | Custom (Streamlit) | 8501 | 8503 |
| `crypto-ia-landing` | Custom (Streamlit) | 8501 | 8504 |
| `crypto-ia-redis` | redis:7-alpine | 6379 | 6385 |

### Production with Gunicorn

```bash
gunicorn api.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

---

## Testing

```bash
# Install test dependencies
pip install -r requirements-api.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test module
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=api --cov-report=term-missing
```

**Test suite: 22 tests across 4 modules**

| Module | Tests | Coverage |
|---|---|---|
| `test_health.py` | 3 | Health check, readiness probe, response format |
| `test_auth.py` | 6 | Register, login, refresh, duplicate email, wrong password, protected endpoint |
| `test_user.py` | 6 | Profile, credits, API keys CRUD, purchase plan |
| `test_analysis.py` | 7 | History, pagination, not found, invalid addresses, auth requirement |

---

## Pricing Plans

| Plan | Price | Credits/mo | Features |
|---|---|---|---|
| **Free** | $0 | 3 | Contract audit, wallet analysis, risk scoring |
| **Basic** | $49/mo | 20 | + Sentiment analysis |
| **Pro** | $199/mo | 100 | + PDF reports, API access, priority support |
| **Enterprise** | Custom | Unlimited | + White-label, SLA, dedicated instance |

---

## Tech Stack

| Category | Technology |
|---|---|
| **API Framework** | FastAPI 0.115+ with async/await |
| **Runtime** | Python 3.12, Uvicorn (ASGI), Gunicorn |
| **Database** | SQLAlchemy 2.0 (async) + aiosqlite / PostgreSQL |
| **Auth** | python-jose (JWT), bcrypt, Pydantic v2 |
| **AI Engine** | OpenAI GPT-4 Turbo |
| **Blockchain** | Web3.py, Etherscan API, CoinGecko API |
| **Payments** | Stripe (webhooks + checkout) |
| **Frontend** | Streamlit 1.51+ |
| **Logging** | structlog (JSON structured) |
| **Containerization** | Docker, Docker Compose |
| **Cache** | Redis 7 |
| **Testing** | pytest, pytest-asyncio, httpx |

---

## Changelog

### [3.0.0] - 2026-02 — Enterprise API

- Full FastAPI REST API with JWT + API Key authentication
- Async database layer (SQLAlchemy 2.0 + aiosqlite)
- Rate limiting, request logging, and error handling middleware
- Structured JSON logging with structlog
- Pydantic v2 request/response validation
- Docker Compose multi-service deployment
- 22 automated tests with pytest-asyncio
- Swagger UI + ReDoc interactive documentation

### [2.0.0] - 2025-12 — SaaS Platform

- Streamlit SaaS frontend with authentication
- Risk scoring engine (0-100)
- Dashboard, credit system, and plan management
- Stripe payment integration
- Landing page
- Report generation

### [1.0.0] - 2025-11 — MVP

- Core analysis modules (contract, wallet, sentiment)
- Etherscan, CoinGecko, NewsAPI connectors
- OpenAI GPT-4 integration
- Basic Streamlit interface

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Disclaimer

This tool provides automated analyses and **does not constitute financial advice**. Always do your own research (DYOR) before investing in any digital asset.
