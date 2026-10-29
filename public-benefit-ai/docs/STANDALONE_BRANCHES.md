# Ten standalone project branches — verifiable remote source

**Verified:** all ten branches exist with a separate root Git tree, dedicated `app/main.py`, one-project `frontend/index.html`, `tests/test_demo.py`, source modules, original project graphics, synthetic fixture, Docker setup and CI workflow. Each branch is within **this existing GitHub repository**, not a new repository.

| # | Exact project | Remote standalone branch |
|---|---|---|
| 1 | AI Disaster Response and Public Safety Assistant | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-ai-disaster-response-public-safety-assistant) |
| 2 | AI Flood and Natural Disaster Early-Warning Support | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-ai-flood-disaster-early-warning) |
| 3 | Emergency Services Information and Coordination Copilot | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-emergency-services-coordination-copilot) |
| 4 | Trusted Public Health Information Assistant | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-trusted-public-health-information-assistant) |
| 5 | AI Road Safety and Accident Hotspot Intelligence | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-ai-road-safety-hotspot-intelligence) |
| 6 | AI Scam, Phishing and Digital Fraud Awareness Assistant | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-scam-phishing-awareness-assistant) |
| 7 | Multilingual Civic Services and Government Scheme Navigator | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-multilingual-civic-services-navigator) |
| 8 | Privacy-Preserving Missing-Person Information Coordination | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-privacy-preserving-missing-person-coordination) |
| 9 | AI Air Quality and Environmental Health Monitor | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-air-quality-environmental-health-monitor) |
| 10 | AI Accessibility and Civic Issue Reporting Platform | [Open branch](https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development/tree/standalone-accessibility-civic-issue-reporting) |

## Clone a single branch (example)

```bash
git clone --single-branch --branch standalone-scam-phishing-awareness-assistant \
  https://github.com/harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development.git scam-demo
cd scam-demo
docker compose up --build
```

Open `http://127.0.0.1:5173` (local UI) or `http://127.0.0.1:8000/docs` (local API). You can also use `python -m pip install -r requirements.txt`, `python -m pytest -q`, and `python cli.py` without Docker.

## Create genuinely distinct repositories

**Not yet done:** independent GitHub remote repository creation. The connected GitHub app lacks the create-repository API; publishing ten branches is not the same operation.

One additional option: a **manually triggered GitHub Actions publisher** has been added in `.github/workflows/publish-ten-github-repositories.yml`. It requires a **GitHub Actions repository secret named `PUBLIC_REPO_CREATION_TOKEN` with account authorization to create public repositories**; the default `GITHUB_TOKEN` cannot create new repositories in your account.

To use: go to repository **Settings → Secrets and variables → Actions**, create the secret (never paste it into chat), then go to **Actions → Create ten independent public GitHub repositories → Run workflow**. The action exports, publishes, and verifies ten repositories. It skips existing names instead of overwriting them. If publishing fails, inspect its job log. Alternatively run `python scripts/export_standalone.py --publish --replace` with authenticated `gh` on your own computer. The secret should be removed/rotated after the one-time operation.

## Production acceptance and safety

These ten are **offline synthetic-data demonstrations**, not authorized operational services. Passing CI establishes runnable basic code checks only. Independent real-world evaluation, approved official data connections, security testing, identity controls, privacy review, domain expert signoff, and externally verified hosting are outstanding. See [acceptance](../docs/ACCEPTANCE.md) and [evaluation](../docs/EVALUATION.md).
