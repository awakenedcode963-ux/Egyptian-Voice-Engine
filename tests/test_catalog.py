from pathlib import Path
import json
import pytest
from egyptian_voice_engine.catalog import VoiceProfile, load_registry

ROOT = Path(__file__).resolve().parents[1]


def test_first_profile():
    p = VoiceProfile.load(ROOT / "voices/voice-001-noura-cairo-feminine/profile.json")
    assert p.voice_id == "eve-egy-001-noura"
    assert p.locale == "ar-EG"
    assert p.sample_rate == 48000
    assert p.status.startswith("profile_design_pending")


def test_registry_unique():
    registry = load_registry(ROOT / "configs/voices.json")
    ids = [v["voice_id"] for v in registry["voices"]]
    assert len(ids) == len(set(ids)) == 1


def test_invalid_sample_rate(tmp_path):
    source = ROOT / "voices/voice-001-noura-cairo-feminine/profile.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data["audio"]["sample_rate"] = 44100
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="sample_rate"):
        VoiceProfile.load(path)
