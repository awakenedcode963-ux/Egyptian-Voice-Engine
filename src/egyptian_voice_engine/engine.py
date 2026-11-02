"""Multi-voice synthesis orchestration with a consent gate and provenance."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import tempfile
import numpy as np

from .catalog import VoiceProfile
from .text.normalizer import NormalizerConfig, normalize_egyptian
from .audio.mastering import write_wav


@dataclass(frozen=True)
class GenerationConfig:
    device: str = "cuda"
    normalize_text: bool = True
    voice_gender: str = "feminine"


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class EgyptianVoiceEngine:
    def __init__(self, profile: VoiceProfile, config=None):
        self.profile = profile
        self.config = config or GenerationConfig()
        self._backend = None

    def _load_backend(self):
        if self._backend is not None: return self._backend
        if self.profile.backend == "namaa_chatterbox":
            from .backends.namaa_chatterbox import NamaaChatterboxBackend
            self._backend = NamaaChatterboxBackend(self.profile.model_id,
                                                    self.profile.model_revision, self.config.device)
        elif self.profile.backend == "habibi":
            from .backends.habibi import HabibiBackend
            opts = self.profile.raw.get("backend_options", {})
            self._backend = HabibiBackend(opts.get("model", "Specialized"),
                                           opts.get("checkpoint"), opts.get("vocab"))
        else:
            raise ValueError(f"Unsupported backend: {self.profile.backend}")
        return self._backend

    def generate(self, text, reference_audio, output_path, reference_text=""):
        ref, out = Path(reference_audio).expanduser().resolve(), Path(output_path).expanduser().resolve()
        if not ref.is_file(): raise FileNotFoundError(f"Reference audio not found: {ref}")
        consent = self.profile.raw.get("reference", {})
        if consent.get("consent_status") != "approved" or not consent.get("consent_record_id"):
            raise PermissionError("Generation blocked until speaker consent is documented and approved")
        clean = normalize_egyptian(text, NormalizerConfig(voice_gender=self.config.voice_gender)) if self.config.normalize_text else text
        backend = self._load_backend()
        with tempfile.TemporaryDirectory(prefix="eve-") as temp:
            raw = Path(temp) / "raw.wav"
            if self.profile.backend == "habibi":
                if not reference_text.strip(): raise ValueError("Habibi requires --reference-text")
                audio, sr = backend.synthesize(clean, str(ref), reference_text, str(raw))
            else:
                audio, sr = backend.synthesize(clean, str(ref))
            stats = write_wav(out, np.asarray(audio, dtype=np.float32), sr,
                              self.profile.sample_rate, self.profile.target_lufs)
        manifest = {
            "schema_version": "1.0", "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "voice_id": self.profile.voice_id, "backend": self.profile.backend,
            "model_id": self.profile.model_id, "model_revision": self.profile.model_revision,
            "normalized_text": clean, "output": str(out), "audio": stats,
            "reference_sha256": _sha256(ref), "output_sha256": _sha256(out),
            "review_status": "pending_human_listening_review", "generation_config": asdict(self.config)
        }
        manifest_path = out.with_suffix(out.suffix + ".manifest.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return manifest
