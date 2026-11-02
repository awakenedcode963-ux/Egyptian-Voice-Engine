#!/usr/bin/env python3
"""Generate a WAV with NAMAA's built-in voice (no reference recording)."""
import argparse
from pathlib import Path
import torchaudio as ta
from huggingface_hub import snapshot_download
from safetensors.torch import load_file
from chatterbox import mtl_tts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="أهلا بيكي، عاملة إيه النهارده؟")
    parser.add_argument("--output", default="outputs/namaa_default_voice.wav")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--revision", default="main")
    args = parser.parse_args()
    model_dir = Path(snapshot_download(repo_id="NAMAA-Space/NAMAA-Egyptian-TTS", repo_type="model", revision=args.revision))
    model = mtl_tts.ChatterboxMultilingualTTS.from_pretrained(device=args.device)
    checkpoint = model_dir / "t3_mtl23ls_v2.safetensors"
    model.t3.load_state_dict(load_file(str(checkpoint), device=args.device), strict=True)
    model.t3.to(args.device).eval()
    audio = model.generate(args.text, language_id="ar")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    ta.save(str(output), audio.detach().float().cpu(), model.sr)
    print(f"Saved {output} ({model.sr} Hz)")

if __name__ == "__main__":
    main()
