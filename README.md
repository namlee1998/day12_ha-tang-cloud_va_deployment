# 🚀 FastAPI Scalable Agent

A production-ready FastAPI service with:
- Redis (state management)
- Rate limiting
- Cost guard
- Docker + Nginx load balancing
- Cloud deployment (Render)

---

## 📦 Requirements

- Docker & Docker Compose
- Git

---

## ⚙️ Environment Variables

Create `.env` file:

```env
REDIS_URL=redis://redis:6379/0
AGENT_API_KEY=secret
RATE_LIMIT_PER_MINUTE=60
MONTHLY_BUDGET_USD=10
LOG_LEVEL=INFO
PORT=8000

Docker:
docker compose up --build --scale agent=3

Test API:
curl http://localhost/health

ASK ENDPOINT:
curl -X POST http://localhost/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secret" \
  -d '{"question": "Hello"}'

Deploy to Render:
Push code to GitHub
Create new Web Service on Render
Set environment variables
Deploy

Security Features
API Key Authentication
Rate Limiting (Redis)
Cost Guard (monthly budget)

Project Structure
app/
  main.py
  config.py
  auth.py
  rate_limiter.py
  cost_guard.py
Dockerfile
docker-compose.yml

Scaling
docker compose up --scale agent=3
