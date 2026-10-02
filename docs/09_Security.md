# 09. Security, RBAC & AI Guardrails

Enterprise AI platforms require defense-in-depth security controls to prevent prompt injection, privilege escalation, catastrophic data loss, and privacy breaches.

---

## 🛡 Security Architecture Highlights

```
   ┌────────────────────────────────────────────────────────┐
   │ 1. INPUT LAYER: Prompt Injection & Adversarial Filter   │
   ├────────────────────────────────────────────────────────┤
   │ 2. AUTH LAYER: HMAC-SHA256 JWT Authentication          │
   ├────────────────────────────────────────────────────────┤
   │ 3. ACCESS LAYER: Role-Based Access Control (RBAC)      │
   ├────────────────────────────────────────────────────────┤
   │ 4. SQL GUARD LAYER: AST & Keyword Whitelist/Blacklist   │
   ├────────────────────────────────────────────────────────┤
   │ 5. RETRIEVAL LAYER: Document & Chunk Clearance Filter   │
   ├────────────────────────────────────────────────────────┤
   │ 6. OUTPUT LAYER: PII Masking & Groundedness Validator  │
   ├────────────────────────────────────────────────────────┤
   │ 7. AUDIT LAYER: Immutable DB Log & Execution Telemetry │
   └────────────────────────────────────────────────────────┘
```

---

## 👥 Role-Based Access Control (RBAC) Matrix

| Capability | EMPLOYEE | ANALYST | MANAGER | ADMIN |
| :--- | :---: | :---: | :---: | :---: |
| Search Public SOPs & Policies | ✅ | ✅ | ✅ | ✅ |
| Execute SQL Analytics | ❌ | ✅ | ✅ | ✅ |
| Access Financial Performance Docs | ❌ | ❌ | ✅ | ✅ |
| View Predictive ML Models & SHAP | ❌ | ✅ | ✅ | ✅ |
| Generate C-Suite Business Reports | ❌ | ❌ | ✅ | ✅ |
| Approve / Reject Workflows (HITL) | ❌ | ❌ | ✅ | ✅ |
| Upload New Corporate Knowledge | ❌ | ❌ | ✅ | ✅ |
| Manage Users & System Config | ❌ | ❌ | ❌ | ✅ |

---

## 🚫 Prompt Injection & Adversarial Defenses
Input queries pass through `AIGuardrails.validate_input()`, filtering out:
- Directive resets (`ignore previous instructions`, `disregard guidelines`).
- System prompt extraction (`leak system prompt`, `reveal instructions`).
- Adversarial jailbreaks (`you are now DAN`, `act as an unfiltered agent`).
- Cross-site scripting & code execution (`<script>`, `exec(...)`).

Queries matching these patterns are immediately rejected with HTTP 400 and flagged in the security audit stream.

---

## 🔒 Safe SQL Gatekeeper
To prevent catastrophic accidental or malicious data modification:
1. **Strict Whitelist**: Queries must match `^(SELECT|WITH)\s`.
2. **Forbidden Blacklist**: Strictly rejects `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`.
3. **No Chained Statements**: Semicolons (`;`) are disallowed to prevent SQL injection chaining.
4. **Read-Only DB User**: In production, the backend connects using a PostgreSQL user granted `CONNECT` and `SELECT` permissions only.

---

## 🤫 PII Redaction
Output text automatically redacts sensitive consumer and financial identifiers:
- Credit Card Numbers: `[REDACTED_CARD_NUMBER]`
- Phone Numbers: `[REDACTED_PHONE_NUMBER]`
- Confidential Passwords / Tokens: `[REDACTED_CREDENTIAL]`
