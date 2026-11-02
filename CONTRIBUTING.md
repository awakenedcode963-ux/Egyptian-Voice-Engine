# Contributing

- Keep model-specific code in backends, dialect rules in text, and speaker-specific settings in voice profiles.
- Never commit reference recordings, signed consent documents, customer audio, private weights or credentials.
- Do not vendor upstream repositories. Use adapters/dependencies and preserve upstream licenses.
- Pin model revisions and package versions for release candidates.
- Include tests, GPU-run evidence, licensing impact, privacy impact and known limitations in pull requests.

Before a PR:
\`\`\`bash
pip install -e ".[dev]"
ruff check .
pytest -q
\`\`\`

New voices require a unique ID, documented consent for synthetic/commercial usage, native Egyptian review, acceptance tests and independent rights checks.
