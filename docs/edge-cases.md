# Edge cases

- **Abandoned OTP flow:** User starts auth then sends unrelated messages. Auth handler keeps state; user can re-send phone or OTP to continue or restart.
- **Invalid messages during auth:** Non-OTP/non-phone input while waiting for OTP or phone is handled with a short prompt to complete the step or type "cancel".
- **Post-login failures:** Payment or inventory errors return a clear message; support/loyalty flows can suggest human handoff.
- **Session timeout:** Sessions expire after inactivity; user is prompted to re-authenticate for sensitive actions (step-up).
- **WhatsApp webhook failures:** Twilio retries; backend should be idempotent and return 200 after processing.
- **Orchestrator/agent unavailable:** API returns 503 or a graceful message; circuit breaker can back off calls to agents.
