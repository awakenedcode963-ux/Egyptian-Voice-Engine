# Egyptian Voice Engine

Open, modular toolkit for building, evaluating and delivering Egyptian Arabic synthetic voices.

## First milestone
A reusable multi-voice foundation and first voice profile: **Noura — Cairo Feminine** (working name). This is an original fictional voice direction, not an imitation of ChatGPT Sol or another real person. The profile is a specification; it is not yet a trained, quality-approved voice asset.

## Principles
- Voice identity and delivery settings live in per-voice profiles; engine code is shared.
- Speaker recordings require explicit permission for synthetic generation and commercial usage.
- Model code, weights, datasets, speaker rights and output rights are reviewed independently.
- Egyptian text normalization is conservative and requires native-speaker review.
- Each generated file receives a provenance manifest and human listening approval.

## Setup
\`\`\`bash
pip install -e ".[dev]"
pytest -q
eve normalize "850 ج وخصم 25%"
\`\`\`

Install the optional NAMAA backend with \`pip install -e ".[namaa]"\`.

After a speaker has explicitly authorized synthetic and commercial use, update a private working copy of the voice profile and run:
\`\`\`bash
eve generate --profile voices/voice-001-noura-cairo-feminine/profile.json --reference-audio /secure/reference.wav --text "أهلا بيكي" --output outputs/noura.wav --device cuda
\`\`\`
The consent gate blocks generation until permission is documented. Never bypass it for convenience.

## Current status
- Multi-voice layout, profile schema, Egyptian normalizer, NAMAA and Habibi adapters, audio mastering, provenance, CI and offline tests: included.
- First voice profile: defined; awaiting an authorized voice-actor recording and native Cairo acceptance tests.
- GPU inference and listening QA: not validated in this repository delivery.
- Commercial release: not approved until all gates in docs/COMMERCIAL_READINESS.md pass.

## Commercial and licensing warning
This repository's MIT license applies only to original code here. It does not license upstream model weights, datasets, reference voices or generated content. NAMAA's model card declares MIT, but exact revisions, dependencies and artifact terms still need review. The MAdel121 Egyptian F5 checkpoint is marked CC BY-NC 4.0 and is excluded from commercial use absent separate permission. See docs/MODEL_AND_LICENSES.md.

## Audio delivery
Default WAV PCM 24-bit / 48 kHz and -14 LUFS integrated for web/social use. This is not EBU R128 broadcast compliance; broadcast programmes commonly target -23 LUFS. The included peak guard is sample-peak, not true-peak limiting.

## Add another voice
Add a profile directory, a unique voice_id, a registry entry, pronunciation overrides and evaluation results. Reuse the same runtime; do not fork it per speaker.

See docs/ARCHITECTURE.md, docs/VOICE_DATA_POLICY.md, docs/COMMERCIAL_READINESS.md and CONTRIBUTING.md.
