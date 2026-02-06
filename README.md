# ABFRL Agentic Commerce

Multi-agent retail system with orchestration, WhatsApp integration, OTP auth, and deployment-ready layout.

## Folder structure (abfrl-agentic-commerce style)

```
├── README.md
├── ARCHITECTURE.md
├── demo/
├── backend/
│   ├── agentic-core/
│   │   ├── master_agent/      # Orchestrator
│   │   ├── worker_agents/     # Inventory, Fulfillment, Payment, Loyalty, Support
│   │   ├── orchestration/
│   │   ├── memory/
│   │   └── risk_engine/       # Circuit breaker, storage, resilience
│   ├── auth-service/         # OTP, session_store, step_up_auth (see integrations/whatsapp)
│   ├── integrations/
│   │   ├── whatsapp/
│   │   ├── payment/
│   │   ├── inventory/
│   │   └── loyalty/
│   └── api-gateway/          # Entry: backend/main.py
├── ai-ml/
│   ├── recommendation/
│   ├── intent-classification/
│   ├── embeddings/
│   └── training/
├── client-apps/
│   ├── mobile-app/ (android, ios)
│   ├── web-app/ (frontend, admin-dashboard)
│   └── kiosk-app/ (ui, session-client, device-auth, offline-mode)
├── infra/
│   ├── docker/
│   ├── env/
│   └── deployment/
└── docs/
    ├── flows/
    ├── edge-cases.md
    ├── security.md
    └── decisions.md
```

## Quick start

- **Backend (local):** `cd backend && pip install -r requirements.txt && python main.py`  
  Or use `start_backend.sh` from repo root.
- **Docker:** `docker-compose -f infra/docker/docker-compose.yml up -d`
- **Deployment:** See `infra/deployment/README.md` and `infra/env/README.md`.

## Docs

- **Architecture:** `ARCHITECTURE.md` and `SYSTEM_EXPLANATION.md`
- **Features:** `FUNCTIONAL_FEATURES.md`
- **Security / edge cases / decisions:** `docs/security.md`, `docs/edge-cases.md`, `docs/decisions.md`
