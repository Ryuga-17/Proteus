# Deployment

## Options

1. **Docker Compose** (staging / single host)  
   From repo root:
   ```bash
   docker-compose -f infra/docker/docker-compose.yml up -d
   ```
   Backend: http://localhost:8000

2. **Kubernetes**  
   - Build image: `docker build -f infra/docker/Dockerfile.backend -t <registry>/abfrl-backend:<tag> .`
   - Push to your registry; deploy via your K8s manifests (Deployment, Service, Ingress).
   - Use secrets for `OPENAI_API_KEY`, Twilio, DB credentials; ConfigMap for non-secret env.

3. **Cloud Run / ECS / App Service**  
   - Use `infra/docker/Dockerfile.backend` as the build context.
   - Set env vars in the platform UI or CI/CD.
   - Expose port 8000; set health check to `/health` or `/docs`.

4. **Local (no Docker)**  
   - `cd backend && pip install -r requirements.txt && python main.py`
   - Or use `start_backend.sh` from repo root.

## Considerations

- **Health:** Backend exposes `/health` (or `/docs`) for load balancers.
- **CORS:** Set `FRONTEND_URL` to your frontend origin(s).
- **WhatsApp webhook:** Point Twilio to `https://<your-domain>/whatsapp/webhook`; set `WHATSAPP_WEBHOOK_VERIFY_TOKEN`.
- **Secrets:** Never commit `.env`; use platform secrets or a vault in production.
