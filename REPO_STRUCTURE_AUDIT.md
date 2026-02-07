# Repository Structure Audit

This document summarizes issues with folder structure, empty/stub folders, misplaced content, and broken references.

---

## Critical issues (broken setup)

### 1. **Proteus_EY/frontend does not exist**

- **start_frontend.sh** and **start_system.sh** use `cd "Proteus_EY/frontend"`.
- There is **no `Proteus_EY` folder** at repo root.
- **Result:** Running `./start_frontend.sh` or `./start_system.sh` fails (directory not found).
- **Actual frontend locations:** `frontend/frontend`, `frontend/frontend2`, `client-apps/web-app`.

**Fix:** Point start scripts to the real frontend, e.g. `frontend/frontend` or `client-apps/web-app`.

---

### 2. **Docs reference wrong path**

- **RUN_SYSTEM.md**, **client-apps/web-app/DEPLOYMENT.md** refer to `Proteus_EY/frontend`.
- Those paths are invalid; they should reference `frontend/frontend` or `client-apps/web-app` as appropriate.

---

## Improper / misplaced structure

### 3. **Frontend inside Inventory agent**

- **Inventory agent/Proteus_EY frontend/** contains a full copy of the Proteus web app (frontend2 variant).
- A full frontend app does not belong inside an agent folder; it makes the repo confusing and duplicates code.
- **Recommendation:** Move or remove this; keep one canonical frontend under `frontend/` or `client-apps/`.

### 4. **Duplicate implementations**

| What | Location 1 | Location 2 | Note |
|------|-------------|------------|------|
| Main web app | `frontend/frontend` | `frontend/frontend2` | Two variants (with/without recommendation API). |
| Main web app | `frontend/frontend` | `client-apps/web-app` | Same app in two places. |
| Kiosk app | `kiosk/` | `kiosk-frontend-api/` | Two kiosk frontend+backend setups. |
| WhatsApp | `whatsapp_integration/` (root) | `backend/integrations/whatsapp/` | Same content; pick one source of truth. |
| Fulfillment agent | `Fullfillment_agent/` (root) | `backend/agentic-core/worker_agents/fulfillment/` | Same domain; root has typo "Fullfillment". |
| Inventory agent | `Inventory agent/` (root) | `backend/agentic-core/worker_agents/inventory/` | Duplicate. |
| Other agents | Root (loyalty, payment, support, etc.) | `backend/agentic-core/worker_agents/` | Same agents in two places. |

**Recommendation:** Choose one place per component (e.g. backend under `backend/`, frontends under `frontend/` or `client-apps/`) and document which is canonical.

---

## Empty or stub folders

### 5. **backend/auth-service** – stubs only

- **backend/auth-service/otp/** – only `__init__.py` (comment references whatsapp `otp_service`).
- **backend/auth-service/session_store/** – only `__init__.py`.
- **backend/auth-service/step_up_auth/** – only `__init__.py`.

No real auth logic here; either implement or remove to avoid confusion.

### 6. **Proteus_EY/frontend** (missing)

- Referenced by scripts and docs but the folder does not exist (see §1).

---

## Naming inconsistencies

### 7. **Spaces vs underscores in folder names**

- With spaces: `Inventory agent`, `loyalty and offers agent`, `Recommendation agent`, `recommendation agent 2`, `post purchase support agent`.
- With underscores: `payment_agent`, `Fullfillment_agent` (also typo).

**Recommendation:** Use one convention (e.g. `snake_case` or `kebab-case`) for all agent/app folders to avoid path and script issues.

### 8. **Typo**

- **Fullfillment_agent** should be **Fulfillment_agent** (or `fulfillment_agent`). Code references this path (e.g. in `orchestrator_tools.py`), so renaming would require updating those references.

---

## Agents: consolidate under backend/agentic-core

**All agents (orchestrator + worker agents) live under `backend/agentic-core/`.**

- **Done:** The orchestrator (both `backend/agentic-core/master_agent` and root `Orchestrator/`) now imports from `backend/agentic-core/worker_agents/` for inventory, fulfillment, payment, loyalty, and support. The five root-level agent folders (`Fullfillment_agent/`, `Inventory agent/`, `payment_agent/`, `loyalty and offers agent/`, `post purchase support agent/`) have been **removed** (contents deleted).
- **Still at root:** `Recommendation agent/` and `recommendation agent 2/` remain at repo root; the orchestrator adds them to path when routing to recommendation. They can be moved into `worker_agents/recommendation/` later.
- **Details:** See **docs/AGENT_CONSOLIDATION.md**.

---

## Suggested canonical layout

A clearer structure could look like:

```
├── backend/                    # Single backend (FastAPI, agents, integrations)
│   ├── agentic-core/           # Orchestrator + all worker agents (single source of truth)
│   │   ├── master_agent/       # Orchestrator
│   │   ├── risk_engine/
│   │   └── worker_agents/      # fulfillment, inventory, loyalty, payment, support, recommendation
│   ├── integrations/          # WhatsApp etc. (remove duplicate at root)
│   ├── main.py
│   └── ...
├── frontend/                   # Main Proteus web app (one folder, e.g. "app" or "proteus")
│   └── ...
├── client-apps/
│   ├── kiosk-app/              # One kiosk app (merge with kiosk-frontend-api if needed)
│   └── web-app/                # Optional alias or link to frontend
├── database/
├── docs/
├── infra/
└── scripts or docs reference  # start_*.sh point to backend/ and frontend/
```

---

## Summary

| Issue | Severity | Action |
|-------|----------|--------|
| Proteus_EY/frontend missing; start scripts broken | **High** | Fix script paths to `frontend/frontend` (or chosen app). |
| Docs reference Proteus_EY/frontend | **High** | Update to correct path. |
| Frontend inside Inventory agent | **Medium** | Move or remove; keep one frontend location. |
| Duplicate WhatsApp / kiosk / agents / web app | **Medium** | Pick canonical locations; document or remove duplicates. |
| backend/auth-service stubs | **Low** | Implement or remove. |
| Folder naming (spaces, Fullfillment typo) | **Low** | Standardize and fix typo when touching those areas. |

After fixing the start scripts and doc paths, run:

- `./start_frontend.sh` → should start the frontend from the chosen folder.
- `./start_system.sh` → should start backend and that same frontend.
