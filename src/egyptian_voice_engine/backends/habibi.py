"""Optional Habibi-TTS EGY adapter for comparison."""
from pathlib import Path
import shutil
import subprocess
import numpy as np
import soundfile as sf


class HabibiBackend:
    def __init__(self, model="Specialized", checkpoint=None, vocab=None):
        if shutil.which("habibi-tts_infer-cli") is None:
            raise RuntimeError("Install Habibi with pip install -e '.[habibi]'")
        self.model, self.checkpoint, self.vocab = model, checkpoint, vocab

    def synthesize(self, text, reference_audio, reference_text, output_path):
        if not reference_text.strip():
            raise ValueError("Habibi requires the exact reference transcript")
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["habibi-tts_infer-cli", "--model", self.model, "--dialect", "EGY",
               "--ref_audio", reference_audio, "--ref_text", reference_text,
               "--gen_text", text, "--output_dir", str(output.parent), "--output_file", output.name]
        if self.checkpoint: cmd += ["--ckpt_file", self.checkpoint]
        if self.vocab: cmd += ["--vocab_file", self.vocab]
        subprocess.run(cmd, check=True)
        audio, sr = sf.read(str(output), dtype="float32", always_2d=False)
        if audio.ndim == 2: audio = audio.mean(axis=1)
        return np.asarray(audio, dtype=np.float32), int(sr)
