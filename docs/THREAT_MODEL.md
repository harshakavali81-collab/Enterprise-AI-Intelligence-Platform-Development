# Threat model — AI Air Quality and Environmental Health Monitor

## Assets / exposed interface

Public JSON API and sample fixtures. This demonstration has no trusted production user registry, external provider keys, live feed or operational resource directory.

## Threats

1. Prompt injection or untrusted source content presented as official instructions.
2. False precision, stale public information, model drift and maliciously crafted examples.
3. Personal-data leakage in case notes or issue photos.
4. API abuse, oversized payloads and untrusted URL handling.
5. Unauthorized action or automation affecting real people.

## Present controls

Synthetic-only data, size constraint, cited demo knowledge base, no autonomous action, no external URL visit, explicit uncertainty, masked/reference-code matching for sensitive demos and mandatory human review.

## Before production

Authenticated authorization, privacy-by-design review, rate limiting, reliable source verification and legal review, secure retention, monitoring and manual operational stop procedures. Special constraint: Missing measurements are not zero pollution; no personalized health advice.
