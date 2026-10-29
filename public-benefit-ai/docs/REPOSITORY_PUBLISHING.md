# Ten independent GitHub repositories: export and publish

**The installed GitHub connection has permission to edit accessible repos but does not provide a create-repository action.** This tool limitation cannot be bypassed by pushing code inside a different repository.

The code in `public-benefit-ai/projects/` can be exported to ten fully independent directory trees, each with its own title, fixture, source modules, APIs, original SVG imagery, tests, and Docker/CI. A shared set of baseline source modules is copied into each export so there is no dependency on the original repository.

## One-time prerequisites

Install Python 3.11+, Git, and the GitHub CLI (`gh`). On your own computer, sign in:

```bash
gh auth login
gh auth status
```

## Run from `public-benefit-ai/`

```bash
python scripts/export_standalone.py
python scripts/export_standalone.py --publish --replace
```

The second command **creates and pushes ten public GitHub repositories** under `harshakavali81-collab` only when GitHub CLI has explicit repository-creation privileges. If a destination already exists, it is *skipped*, never overwritten. Do not commit secrets, actual missing-person reports or private user data.

## Exact repository names

1. `AI-Disaster-Response-and-Public-Safety-Assistant`
2. `AI-Flood-and-Natural-Disaster-Early-Warning-Support`
3. `Emergency-Services-Information-and-Coordination-Copilot`
4. `Trusted-Public-Health-Information-Assistant`
5. `AI-Road-Safety-and-Accident-Hotspot-Intelligence`
6. `AI-Scam-Phishing-and-Digital-Fraud-Awareness-Assistant`
7. `Multilingual-Civic-Services-and-Government-Scheme-Navigator`
8. `Privacy-Preserving-Missing-Person-Information-Coordination`
9. `AI-Air-Quality-and-Environmental-Health-Monitor`
10. `AI-Accessibility-and-Civic-Issue-Reporting-Platform`

These are **planned** repository names, not links to verified existing repositories. Once created, update the portfolio cards to reference actual repository URLs, not guessed URLs.

The exported prototypes are not validated public services; publishing code does not grant operational approval.
