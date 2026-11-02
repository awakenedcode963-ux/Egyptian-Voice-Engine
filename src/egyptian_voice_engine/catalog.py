"""Load and validate voice profiles."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class VoiceProfile:
    voice_id: str
    display_name: str
    locale: str
    dialect: str
    backend: str
    model_id: str
    model_revision: str
    sample_rate: int
    target_lufs: float
    status: str
    raw: dict[str, Any]

    @classmethod
    def load(cls, path: str | Path) -> "VoiceProfile":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for field in ("voice_id", "display_name", "locale", "dialect", "backend", "model_id"):
            if not data.get(field):
                raise ValueError(f"Missing profile field: {field}")
        audio = data.get("audio", {})
        sr = int(audio.get("sample_rate", 48000))
        if sr not in (24000, 48000):
            raise ValueError("audio.sample_rate must be 24000 or 48000")
        return cls(
            voice_id=data["voice_id"], display_name=data["display_name"],
            locale=data["locale"], dialect=data["dialect"], backend=data["backend"],
            model_id=data["model_id"], model_revision=data.get("model_revision", "main"),
            sample_rate=sr, target_lufs=float(audio.get("target_lufs", -14)),
            status=data.get("status", "draft"), raw=data,
        )


def load_registry(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    voices = data.get("voices")
    if not isinstance(voices, list):
        raise ValueError("Registry must contain a voices list")
    ids = [item.get("voice_id") for item in voices]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate voice_id in registry")
    return data
