"""Resampling, loudness normalization and PCM WAV export."""
from math import gcd
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


def normalize_loudness(audio, sample_rate, target_lufs=-14.0, peak_ceiling_dbfs=-1.0):
    try:
        import pyloudnorm as pyln
    except ImportError as exc:
        raise RuntimeError("Install pyloudnorm to measure integrated loudness") from exc
    data = np.asarray(audio, dtype=np.float32).reshape(-1)
    if len(data) < sample_rate // 4 or not np.isfinite(data).all():
        raise ValueError("Audio too short or contains non-finite samples")
    meter = pyln.Meter(sample_rate)
    before = float(meter.integrated_loudness(data))
    if not np.isfinite(before):
        raise ValueError("Loudness measurement failed; input may be silent")
    result = pyln.normalize.loudness(data, before, target_lufs).astype(np.float32)
    ceiling = 10 ** (peak_ceiling_dbfs / 20)
    peak = float(np.max(np.abs(result)))
    if peak > ceiling: result *= ceiling / peak
    after = float(meter.integrated_loudness(result))
    peak_dbfs = 20 * np.log10(max(float(np.max(np.abs(result))), 1e-12))
    return result, {"input_lufs": before, "output_lufs": after,
                    "target_lufs": target_lufs, "sample_peak_dbfs": float(peak_dbfs)}


def write_wav(path, audio, source_sr, target_sr=48000, target_lufs=-14.0):
    if source_sr <= 0 or target_sr not in (24000, 48000):
        raise ValueError("Unsupported sample rate")
    data = np.asarray(audio, dtype=np.float32).reshape(-1)
    if source_sr != target_sr:
        factor = gcd(source_sr, target_sr)
        data = resample_poly(data, target_sr // factor, source_sr // factor).astype(np.float32)
    data, stats = normalize_loudness(data, target_sr, target_lufs)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), data, target_sr, subtype="PCM_24")
    stats.update({"sample_rate": target_sr, "duration_seconds": len(data) / target_sr})
    return stats
