from pathlib import Path
import pytest

from egyptian_voice_engine.catalog import VoiceProfile
from egyptian_voice_engine.engine import EgyptianVoiceEngine

ROOT = Path(__file__).resolve().parents[1]


def test_generation_is_blocked_without_recorded_consent(tmp_path):
    profile = VoiceProfile.load(ROOT / "voices/voice-001-noura-cairo-feminine/profile.json")
    reference = tmp_path / "dummy.wav"
    reference.write_bytes(b"not-real-audio")
    engine = EgyptianVoiceEngine(profile)

    with pytest.raises(PermissionError, match="consent"):
        engine.generate("أهلا بيكي", reference, tmp_path / "out.wav")

    # The backend must not load before the consent check.
    assert engine._backend is None
