# Egyptian Voice Engine

Open, modular toolkit for building, evaluating, and delivering Egyptian Arabic synthetic voices.

## Current milestone
A reusable multi-voice platform and its first voice profile: **Noura — Cairo Feminine** (working name). The profile is a specification, not a claim that a trained or production-approved voice asset already exists.

## Principles
- Voice identity and settings live in per-voice profiles; shared code is reusable.
- A speaker reference requires explicit consent for synthetic generation and commercial use.
- Model code, weights, training data, reference voices, and output rights are reviewed independently.
- Egyptian text normalization is conservative and reviewed by native speakers.
- Generated files carry provenance manifests and require listening approval.

## Quick start
```bash
pip install -e ".[dev]"
pytest -q
eve normalize "850 ج وخصم 25%"
```

## First voice
Profile: `voices/voice-001-noura-cairo-feminine/profile.json`

The profile awaits an authorized reference recording and native-speaker acceptance testing. It contains no voice recording or model weights. The engine blocks generation until the profile's consent state is explicitly approved after permission is documented.

## Generate (after authorized reference and GPU setup)
```bash
pip install -e ".[namaa]"
eve generate --profile voices/voice-001-noura-cairo-feminine/profile.json --reference-audio /secure/local/reference.wav --text "أهلا بيكي" --output outputs/noura.wav --device cuda
```

## Model rights
The project's MIT license applies only to original code. It does not grant rights to upstream models, model weights, datasets, reference recordings, or generated content. The MAdel121 Egyptian F5 checkpoint is marked CC BY-NC 4.0 and is excluded from commercial use absent separate permission. See `docs/MODEL_AND_LICENSES.md` and `docs/COMMERCIAL_READINESS.md`.

## Delivery status
Code structure, normalizer, profile schema, audio utilities, engine orchestration, CI, docs, and tests are included. GPU inference, actual reference recordings, model-specific quality acceptance, and commercial approval remain outstanding. No audio is fabricated or represented as generated when inference has not run.

See the detailed README and documentation in this repository for architecture, evaluation, consent, and roadmap.
