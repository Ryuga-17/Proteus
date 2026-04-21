#  ABFRL Agentic Commerce System

A comprehensive, production-ready multi-agent retail management system built with CrewAI. This project replaces traditional monolithic e-commerce backends with a smart, autonomous **Agentic Core** where distinct AI agents own specific retail domains, all coordinated seamlessly by a central Orchestrator.

##  What is this system doing?

At its core, the system acts as a highly intelligent retail backend that processes natural language requests, complex transactions, and omnichannel interactions through specialized AI agents. 

When a request comes in—whether through the physical kiosk, a WhatsApp message, or the frontend website—it hits the **Orchestrator Agent**. The Orchestrator performs intent analysis, breaks down the request, and delegates tasks to specific **Worker Agents**, synthesizing their outputs into a cohesive response for the user.

###  The Agent Team
* ** Orchestrator Agent (Master)**: The central command hub. All requests flow through here. It routes tasks, coordinates multi-agent workflows, and handles unified responses.
* ** Inventory Agent**: Checks stock across godowns and stores, handles logistics/transfers, and triggers procurement from suppliers.
* ** Fulfillment Agent**: Manages ship-to-home deliveries, in-store item reservations, and alerts staff.
* ** Payment Agent**: Securely processes standard payments, UPI, handles kiosk-to-mobile payment handoffs via QR code, and connects to loyalty for point deductions.
* ** Loyalty & Offers Agent**: Expertly calculates complex pricing, applying coupon discounts, and tracking loyalty points.
* ** Post-Purchase Support Agent**: Takes care of the customer post-sale—tracking shipments, processing returns/exchanges, and sending feedback surveys.
* ** Recommendation Agents (v1 & v2)**: Powers voice search and personalization using real LLM embeddings (Ollama) and vector search (Qdrant).

##  Key Features

* **Omnichannel Interfaces**:
  * **WhatsApp Integration**: Complete messaging bot with secure OTP account linking, step-up authentication for high-risk operations, and persistent sessions.
  * **Kiosk App**: Physical store interface featuring dynamic QR-code-based session linking to the user's mobile device.
  * **Web Frontend**: A React + TypeScript interface with voice search capabilities and a modern shopping experience.
* **Advanced AI Features**:
  * AI-powered Size & Fit recommendations based on preferences.
  * Virtual Try-On API integrating the Nano Banana model.
* **Production MLOps Pipeline ("Antigravity" Style)**:
  * **Automated Training Loop**: APScheduler handles background jobs for compiling JSON-based ML Event logs and evaluating candidate models.
  * **Evaluation & Promotion Logic**: Seamless tracking of CTR and Conversion metrics to promote models safely without manual intervention.
  * **Registry & Rollback**: Uses `model_registry_manager` to support active versioning, graceful dynamic component loading, and explicit rollbacks for failing configurations.
* **Enterprise Resilience**: Built-in circuit breakers, payment idempotency, persistent fallback queues, soft reservations with TTL, and robust database operations via PostgreSQL.

##  Repository Structure

```
├── README.md                  # This file
├── SYSTEM_EXPLANATION.md      # Deep dive into agent mechanisms and flows
├── ARCHITECTURE.md            # Technical architecture and component map
├── FUNCTIONAL_FEATURES.md     # Exhaustive list of all capabilities
├── RUN_SYSTEM.md              # Detailed running and troubleshooting guide
├── backend/
│   ├── agentic-core/          # Orchestrator & Worker Agents logic
│   ├── auth-service/          # OTP, sessions, step-up auth
│   ├── integrations/          # WhatsApp, Payments, Inventory hooks
│   └── main.py                # FastAPI API Gateway
├── ai-ml/                     # Embeddings, intent-classification, recommendations
│   ├── features/              # Feature Store (Caching & Lazy loading)
│   ├── monitoring/            # Explicit historical CTR/Conversion metrics calculation
│   ├── pipelines/             # Auto-data cleanup and Auto-training/eval scripts
│   └── model_registry.json    # JSON-based model registry with rollback support
├── client-apps/
│   ├── web-app/               # React + TS frontend
│   └── kiosk-app/             # In-store display interfaces
├── infra/                     # Dockerfiles, docker-compose, and deployment configs
└── docs/                      # Security, edge cases, and design decisions
```

##  Quick Start

### The Easiest Way
Run everything (Frontend + Backend) with a single script:
```bash
./start_system.sh
```

### Manual Start
**Terminal 1 - Backend:**
```bash
./start_backend.sh
# Alternatively: cd backend && pip install -r requirements.txt && python main.py
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
# Alternatively: cd Proteus_EY/frontend && npm install && npm run dev
```

### Docker
```bash
docker-compose -f infra/docker/docker-compose.yml up -d
```

##  Access Points
- **Frontend UI**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

##  Further Reading
To truly understand how to operate, deploy, or extend this system, please review the extensive documentation provided:
- **System Overview & Agent Workflows**: `SYSTEM_EXPLANATION.md`
- **Complete Features List**: `FUNCTIONAL_FEATURES.md`
- **Architecture Insights**: `ARCHITECTURE.md`
- **Advanced Running/Testing Instructions**: `RUN_SYSTEM.md`
