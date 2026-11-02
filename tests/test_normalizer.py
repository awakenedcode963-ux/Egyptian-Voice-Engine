from egyptian_voice_engine.text.normalizer import normalize_egyptian, number_to_egyptian, NormalizerConfig


def test_price():
    assert "تمنمية وخمسين جنيه" in normalize_egyptian("850 ج")


def test_percentage():
    assert normalize_egyptian("خصم 25%") == "خصم خمسة وعشرين في المية"


def test_arabic_digits_and_tanween():
    result = normalize_egyptian("سعر ٨٥٠ ج جميلٌ")
    assert "تمنمية وخمسين جنيه" in result
    assert "ٌ" not in result


def test_colloquial_now():
    assert normalize_egyptian("احجزي الآن") == "احجزي دلوقتي"


def test_gender_option():
    assert "تقدر" in normalize_egyptian("يمكنك الحجز", NormalizerConfig(voice_gender="masculine"))


def test_phone_preserved():
    assert "01012345678" in normalize_egyptian("واتساب 01012345678")


def test_number_words():
    assert number_to_egyptian(850) == "تمنمية وخمسين"
    assert number_to_egyptian(25) == "خمسة وعشرين"
    assert number_to_egyptian(1000) == "ألف"


def test_no_final_sukun_insertion():
    assert "ٌ" not in normalize_egyptian("البشرة جميلةٌ")
