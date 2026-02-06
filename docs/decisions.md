# Architecture decisions

- **Channel-agnostic core:** WhatsApp (and future channels) are integrations; orchestration, auth, and business logic live in the backend so new channels can reuse the same flow.
- **Dual structure during migration:** Backend supports both the new layout (`backend/agentic-core`, `backend/integrations/whatsapp`) and legacy paths (`resilience`, `whatsapp_integration`, `Orchestrator`) so migration can be gradual.
- **File-backed resilience for demo:** Inventory, orders, payments use JSON file stores for demo; production should use a database (PostgreSQL) and optional queues.
- **Deployment:** Docker and deployment docs live under `infra/` so all deployment concerns (Docker, env, deployment) are in one place.
