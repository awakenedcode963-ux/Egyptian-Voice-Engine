# NAMAA setup and first inference

- Model: https://huggingface.co/NAMAA-Space/NAMAA-Egyptian-TTS
- Architecture: Chatterbox Multilingual, 0.5B parameters
- Model card license declaration: MIT
- Dialect: Egyptian Arabic, language_id="ar"

## Free inference
1. Kaggle Notebook with a free GPU accelerator when available.
2. Local GPU.
3. CPU for a functional smoke test, but expect slow generation.

Free/open model weights do not imply unlimited hosted compute.

## Local quickstart
    pip install -e ".[namaa]"
    python scripts/namaa_smoke_test.py --text "أهلا بيكي، عاملة إيه النهارده؟" --output outputs/namaa_default_voice.wav --device cuda

## Kaggle
Open notebooks/NAMAA_Kaggle_Quickstart.ipynb, enable GPU if offered, and run all cells. First run downloads the checkpoint.

## Reference audio
NAMAA supports audio_prompt_path. Only use a person's voice with explicit permission for synthetic generation and intended commercial use. Never commit reference recordings or consent evidence.

## Known limitations
The upstream card warns that ق may be mispronounced, numbers may be wrong, and flow may vary with reference prompts. Test numbers, prices, negation, names and medical vocabulary manually.

## Reproducibility
Before production, pin an immutable Hugging Face commit, package versions and GPU details. The quickstart uses main for ease of first setup and is not a release lockfile.
