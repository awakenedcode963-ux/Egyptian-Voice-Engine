# Egyptian Voice Engine

Modular toolkit for Egyptian Arabic synthetic voices.

## First runnable backend: NAMAA Egyptian TTS
The first backend is NAMAA-Space/NAMAA-Egyptian-TTS, based on Chatterbox Multilingual. It supports Egyptian Arabic and a built-in voice, plus optional authorized reference-audio prompting.

### Free first test
Open notebooks/NAMAA_Kaggle_Quickstart.ipynb. Choose a free GPU accelerator if available, run all cells, and listen to the WAV output. Kaggle controls GPU availability and quotas; they can vary. Model weights are publicly available under the model card's stated MIT license.

### Local install
    pip install -e ".[namaa]"
    python scripts/namaa_smoke_test.py --text "أهلا بيكي، عاملة إيه النهارده؟" --output outputs/namaa_default_voice.wav --device cuda

CPU is supported by the upstream model but can be very slow.

### Reference voice
Only use a recording when its speaker explicitly agreed to synthetic generation and intended commercial use. Keep recordings and consent evidence private. The main engine's reference-voice workflow remains consent-gated.

## Quality and rights
The NAMAA model card declares MIT and commercial use with attribution. Review the exact model revision, base Chatterbox dependency and package terms before production. The model card warns of possible errors in ق, numbers and text/audio consistency. Native Egyptian listening QA is mandatory.

The repository MIT license covers only original project code. It does not grant rights to a speaker's voice or unrelated datasets. Do not claim this is a clone of ChatGPT's Sol. Noura is an original voice direction, not a trained voice identity.

See docs/NAMAA_SETUP.md, docs/MODEL_AND_LICENSES.md, docs/COMMERCIAL_READINESS.md and docs/VOICE_DATA_POLICY.md.
