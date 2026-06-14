import pytest

from octalume.idea.parser import parse_brain_dump


def test_empty_input_raises():
    with pytest.raises(ValueError):
        parse_brain_dump("")


def test_title_from_heading():
    p = parse_brain_dump("# My Cool App\n\nA short description.")
    assert p.title == "My Cool App"


def test_title_fallback_to_first_line():
    p = parse_brain_dump("Just a thing I want to build.\n\nWith more details.")
    assert p.title.startswith("Just a thing")


def test_domain_detection_saas():
    text = "# App\n\nA SaaS app with users, subscription billing via Stripe and a dashboard."
    p = parse_brain_dump(text)
    assert p.primary_domain == "saas"


def test_domain_detection_iot():
    text = "# Sensor\n\nESP32 sensor with MQTT and firmware over GPIO."
    p = parse_brain_dump(text)
    assert p.primary_domain == "iot"


def test_bullets_classified_into_risks_and_features():
    text = """# X

- ship a login page
- risk: secrets might leak
- unclear: which DB should we use?
"""
    p = parse_brain_dump(text)
    assert any("login" in f.lower() for f in p.features)
    assert any("secret" in r.lower() for r in p.risks)
    assert any("db" in u.lower() or "which" in u.lower() for u in p.unknowns)


def test_slug_is_url_safe():
    p = parse_brain_dump("# Hello, World!! v2\n\nbody")
    assert p.slug == "hello-world-v2"


def test_inline_questions_become_unknowns():
    p = parse_brain_dump("# X\n\nShould we use Postgres?\n")
    assert any("Postgres" in u for u in p.unknowns)
