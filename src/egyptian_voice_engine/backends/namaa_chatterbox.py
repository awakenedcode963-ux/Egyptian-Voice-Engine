"""NAMAA Egyptian fine-tune adapter for Chatterbox Multilingual."""
from pathlib import Path
import numpy as np


class NamaaChatterboxBackend:
    def __init__(self, model_id: str, revision: str = "main", device: str = "cuda"):
        try:
            from huggingface_hub import snapshot_download
            from safetensors.torch import load_file
            from chatterbox import mtl_tts
        except ImportError as exc:
            raise RuntimeError('Install with pip install -e ".[namaa]"') from exc
        model_dir = Path(snapshot_download(repo_id=model_id, repo_type="model", revision=revision))
        checkpoint = model_dir / "t3_mtl23ls_v2.safetensors"
        if not checkpoint.is_file():
            raise FileNotFoundError(f"NAMAA T3 checkpoint not found: {checkpoint}")
        self.model = mtl_tts.ChatterboxMultilingualTTS.from_pretrained(device=device)
        self.model.t3.load_state_dict(load_file(str(checkpoint), device=device), strict=True)
        self.model.t3.to(device).eval()

    def synthesize(self, text: str, reference_audio: str):
        wave = self.model.generate(text, language_id="ar", audio_prompt_path=reference_audio,
                                   exaggeration=0.5, cfg_weight=0.5)
        if hasattr(wave, "detach"):
            wave = wave.detach().float().cpu().numpy()
        audio = np.asarray(wave, dtype=np.float32).squeeze()
        if audio.ndim != 1 or not audio.size:
            raise RuntimeError("NAMAA returned empty or unsupported audio")
        return audio, int(self.model.sr)
