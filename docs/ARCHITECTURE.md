# Architecture

The repository separates:
1. Voice catalog: per-voice style, dialect, backend/model, consent state and output settings.
2. Text layer: Egyptian Arabic spelling, number and phrase normalization.
3. Backend layer: optional adapters; heavy dependencies load only when selected.
4. Engine layer: consent gate, synthesis, mastering, output and provenance.

Flow: script -> normalize -> resolve voice profile -> consent gate -> model adapter -> raw audio -> resample/loudness/WAV -> hashes/manifest -> native-speaker review.

New voices add a profile, registry entry, lexicon and evaluation results; they reuse the same engine. They do not require copying the runtime.

Limitations: GPU inference has not been validated in this repository delivery; normalization is not a full dialect translator; reference conditioning cannot guarantee exact or consistent speaker identity across long scripts.
