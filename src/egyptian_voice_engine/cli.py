"""Command-line interface."""
import argparse
import json
from .catalog import VoiceProfile
from .engine import EgyptianVoiceEngine, GenerationConfig
from .text.normalizer import NormalizerConfig, normalize_egyptian


def main():
    parser = argparse.ArgumentParser(prog="eve")
    sub = parser.add_subparsers(dest="command", required=True)
    norm = sub.add_parser("normalize")
    norm.add_argument("text", nargs="+")
    norm.add_argument("--gender", choices=["feminine", "masculine", "neutral"], default="feminine")
    gen = sub.add_parser("generate")
    gen.add_argument("--profile", required=True)
    gen.add_argument("--reference-audio", required=True)
    gen.add_argument("--reference-text", default="")
    gen.add_argument("--text", required=True)
    gen.add_argument("--output", default="outputs/generated.wav")
    gen.add_argument("--device", default="cuda")
    args = parser.parse_args()
    if args.command == "normalize":
        print(normalize_egyptian(" ".join(args.text), NormalizerConfig(voice_gender=args.gender)))
        return
    profile = VoiceProfile.load(args.profile)
    result = EgyptianVoiceEngine(profile, GenerationConfig(device=args.device)).generate(
        args.text, args.reference_audio, args.output, args.reference_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
