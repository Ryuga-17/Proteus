# Security

- **Secrets:** All API keys (OpenAI, Twilio, DB) and tokens live in environment variables or a vault; never in code or committed files. Use `.env.example` as a template; `.env` is gitignored.
- **OTP:** 6-digit OTP with short expiry; rate-limit send/verify to prevent abuse.
- **Step-up auth:** High-risk actions (payments, refunds, address changes) require re-verification (e.g. OTP) before proceeding.
- **Webhook verification:** WhatsApp webhook uses `WHATSAPP_WEBHOOK_VERIFY_TOKEN`; validate in GET and verify request source in POST (Twilio signature when available).
- **CORS:** Set `FRONTEND_URL` to allowed origins only.
- **Data:** Persist only what’s needed (sessions, OTPs); avoid logging PII or full message bodies in production.
