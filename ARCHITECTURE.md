# Architecture

## Overview

- **API gateway:** `backend/main.py` – FastAPI app; mounts core API and WhatsApp at `/whatsapp`.
- **Agentic core:** `backend/agentic-core/` – Master agent (orchestrator) in `master_agent/`, worker agents in `worker_agents/`, resilience in `risk_engine/`. Legacy equivalents: `Orchestrator/`, `resilience/`, and root-level agents.
- **Integrations:** `backend/integrations/whatsapp/` – WhatsApp webhook, OTP auth, session store, step-up auth. Legacy: `whatsapp_integration/`.
- **AI/ML:** `ai-ml/recommendation/` – Recommendation and related models; intent-classification, embeddings, training are placeholders.
- **Client apps:** `client-apps/web-app/frontend/`, `client-apps/kiosk-app/` – Web and kiosk UIs; mobile placeholders under `mobile-app/`.
- **Infra:** `infra/docker/` (Dockerfile, docker-compose), `infra/env/`, `infra/deployment/` – Deployment and env configuration.

## Request flow

1. **WhatsApp:** Twilio → POST `/whatsapp/webhook` → auth/session check → message handler → orchestrator (if authenticated) → worker agents → response via Twilio.
2. **REST:** Frontend/Kiosk → backend (recommendations, inventory, purchase, etc.) → resilience/risk_engine and agents as needed.

## Deployment

- **Docker:** Build with `infra/docker/Dockerfile.backend`; run with `infra/docker/docker-compose.yml`. Backend listens on 8000.
- **Secrets:** Use env (or vault); see `infra/env/README.md` and `docs/security.md`.
- **Health:** Backend exposes `/docs` and (if implemented) `/health` for load balancers.

See `infra/deployment/README.md` for Kubernetes, Cloud Run, and local options.
