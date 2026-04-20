import pytest
from src.core.disclaimer import (
    get_disclaimer,
    DISCLAIMER_EN,
    DISCLAIMER_ES,
    SHORT_DISCLAIMER_EN,
    SHORT_DISCLAIMER_ES,
    CRIMINAL_WARNING_EN,
    CRIMINAL_WARNING_ES,
    PLEA_WARNING_EN,
    PLEA_WARNING_ES
)

def test_get_disclaimer_standard():
    assert get_disclaimer("en", "standard") == DISCLAIMER_EN
    assert get_disclaimer("es", "standard") == DISCLAIMER_ES

def test_get_disclaimer_short():
    assert get_disclaimer("en", "short") == SHORT_DISCLAIMER_EN
    assert get_disclaimer("es", "short") == SHORT_DISCLAIMER_ES

def test_get_disclaimer_criminal():
    assert get_disclaimer("en", "criminal") == CRIMINAL_WARNING_EN
    assert get_disclaimer("es", "criminal") == CRIMINAL_WARNING_ES

def test_get_disclaimer_plea():
    assert get_disclaimer("en", "plea") == PLEA_WARNING_EN
    assert get_disclaimer("es", "plea") == PLEA_WARNING_ES

def test_get_disclaimer_default_level():
    # If level is not provided, it should default to "standard"
    assert get_disclaimer("en") == DISCLAIMER_EN
    assert get_disclaimer("es") == DISCLAIMER_ES

def test_get_disclaimer_language_fallback():
    # Any language other than "es" should fall back to "en"
    assert get_disclaimer("fr", "standard") == DISCLAIMER_EN
    assert get_disclaimer("de", "short") == SHORT_DISCLAIMER_EN
    assert get_disclaimer("unknown") == DISCLAIMER_EN

def test_get_disclaimer_unknown_level():
    # Unknown level should fall back to DISCLAIMER_EN
    assert get_disclaimer("en", "unknown_level") == DISCLAIMER_EN
    # Note: currently the function falls back to DISCLAIMER_EN even if lang is "es"
    assert get_disclaimer("es", "unknown_level") == DISCLAIMER_EN
