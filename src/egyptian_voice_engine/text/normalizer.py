"""Conservative Egyptian Arabic TTS text normalization."""
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Mapping

_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
_UNITS = ["صفر", "واحد", "اتنين", "تلاتة", "أربعة", "خمسة", "ستة", "سبعة", "تمانية", "تسعة"]
_TEENS = ["عشرة", "حداشر", "اتناشر", "تلتاشر", "أربعتاشر", "خمستاشر", "ستاشر", "سبعتاشر", "تمنتاشر", "تسعتاشر"]
_TENS = {20:"عشرين",30:"تلاتين",40:"أربعين",50:"خمسين",60:"ستين",70:"سبعين",80:"تمانين",90:"تسعين"}
_HUNDREDS = {100:"مية",200:"ميتين",300:"تلتمية",400:"ربعمية",500:"خمسمية",600:"ستمية",700:"سبعمية",800:"تمنمية",900:"تسعمية"}
_DEFAULT = {"في الوقت الحالي":"دلوقتي","الآن":"دلوقتي","حاليًا":"دلوقتي","حالياً":"دلوقتي","يمكنك":"تقدري","بإمكانك":"تقدري","ينبغي":"لازم","يجب عليك":"لازم","احجزي الآن":"احجزي دلوقتي","احجز الآن":"احجز دلوقتي"}


@dataclass(frozen=True)
class NormalizerConfig:
    voice_gender: str = "feminine"
    convert_numbers: bool = True
    strip_diacritics: bool = True
    colloquialize_common_phrases: bool = True
    preserve_phone_numbers: bool = True
    custom_replacements: Mapping[str, str] = field(default_factory=dict)


def _under_100(n):
    if n < 10: return _UNITS[n]
    if n < 20: return _TEENS[n-10]
    tens, unit = divmod(n, 10)
    return _TENS[tens*10] if not unit else f"{_UNITS[unit]} و{_TENS[tens*10]}"


def _under_1000(n):
    if n < 100: return _under_100(n)
    hundreds, rest = divmod(n, 100)
    base = _HUNDREDS[hundreds*100]
    return base if not rest else f"{base} و{_under_100(rest)}"


def number_to_egyptian(n: int) -> str:
    if not isinstance(n, int) or n < 0 or n > 999_999_999:
        raise ValueError("number must be 0..999,999,999")
    if n < 1000: return _under_1000(n)
    thousands, rest = divmod(n, 1000)
    prefix = "ألف" if thousands == 1 else "ألفين" if thousands == 2 else f"{_UNITS[thousands]} تلاف" if thousands < 11 else f"{number_to_egyptian(thousands)} ألف"
    return prefix if not rest else f"{prefix} و{_under_1000(rest)}"


def _decimal_words(value):
    value = value.replace("٫", ".").replace(",", ".")
    if "." not in value: return number_to_egyptian(int(value))
    whole, fraction = value.split(".", 1)
    return number_to_egyptian(int(whole or "0")) + " فاصلة " + " ".join(number_to_egyptian(int(x)) for x in fraction if x.isdigit())


def normalize_egyptian(text: str, config: NormalizerConfig | None = None) -> str:
    if not isinstance(text, str): raise TypeError("text must be a string")
    cfg = config or NormalizerConfig()
    result = unicodedata.normalize("NFC", text).translate(_ARABIC_DIGITS)
    if cfg.strip_diacritics: result = _DIACRITICS.sub("", result)
    if cfg.colloquialize_common_phrases:
        replacements = dict(_DEFAULT)
        if cfg.voice_gender == "masculine": replacements.update({"يمكنك":"تقدر","بإمكانك":"تقدر"})
        if cfg.voice_gender == "neutral": replacements.update({"يمكنك":"ممكن","بإمكانك":"ممكن"})
        replacements.update(cfg.custom_replacements)
        for src in sorted(replacements, key=len, reverse=True): result = result.replace(src, replacements[src])
    if cfg.convert_numbers:
        pct = re.compile(r"(?<!\w)(\d+(?:[.,٫]\d+)?)\s*%")
        result = pct.sub(lambda m: _decimal_words(m.group(1)) + " في المية", result)
        price = re.compile(r"(?<!\w)(\d+(?:[.,٫]\d+)?)\s*(جنيه\s+مصري|جنيه(?:ات)?|ج|EGP)(?=$|[^\w])", re.I)
        result = price.sub(lambda m: _decimal_words(m.group(1)) + " جنيه", result)
        protected = {}
        if cfg.preserve_phone_numbers:
            def keep(m):
                key = f"ZXQPHONE{len(protected)}QXZ"; protected[key] = m.group(0); return key
            result = re.sub(r"(?<!\w)\+?\d[\d\s()-]{8,}\d(?!\w)", keep, result)
        result = re.sub(r"(?<![\w])\d+(?:[.,٫]\d+)?(?![\w])", lambda m: _decimal_words(m.group(0)), result)
        for k, v in protected.items(): result = result.replace(k, v)
    result = re.sub(r"[ \t\u00a0]+", " ", result)
    result = re.sub(r"\s+([،؛,.!?؟])", r"\1", result)
    return result.strip()


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="+")
    p.add_argument("--gender", choices=["feminine","masculine","neutral"], default="feminine")
    a = p.parse_args()
    print(normalize_egyptian(" ".join(a.text), NormalizerConfig(voice_gender=a.gender)))


if __name__ == "__main__": main()
