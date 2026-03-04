# Worker agents

All individual agents and their logic live here. The orchestrator (master_agent / orchestration) routes requests to these workers.

| Worker | Role |
|--------|------|
| **fulfillment** | Shipping, reservations, pickup |
| **inventory** | Stock levels, transfers, procurement |
| **loyalty** | Pricing, discounts, coupons, points |
| **payment** | Payments, kiosk handoff (with sales + loyalty) |
| **support** | Order tracking, returns, exchanges, feedback |
| **recommendation_agent1** | Product recommendations (CrewAI agent) |
| **recommendation_agent2** | Voice/product recommendations (Ollama, Qdrant, voice_processor_v2) |

- **API / voice recommendations:** Backend uses `recommendation_agent2` for `/api/recommendations/voice` and product/category data.
- **Orchestrator routing:** `orchestrator_tools` route to each worker by name (e.g. `route_to_recommendation` → recommendation_agent1, `route_to_recommendation_v2` → recommendation_agent2).
