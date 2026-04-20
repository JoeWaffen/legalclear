import pytest
from unittest.mock import patch
from core.i18n import get_lang, translate_if_needed

def test_get_lang_with_user_preference():
    assert get_lang("en", "es") == "es"
    assert get_lang("es", "en") == "en"

def test_get_lang_with_invalid_user_preference():
    assert get_lang("es", "fr") == "es"
    assert get_lang("en", "de") == "en"

def test_get_lang_with_detected():
    assert get_lang("es") == "es"
    assert get_lang("en") == "en"

def test_get_lang_unsupported_languages():
    assert get_lang("fr", "de") == "en"
    assert get_lang("fr") == "en"
    assert get_lang("de", "it") == "en"

def test_translate_if_needed_not_es():
    assert translate_if_needed("Hello", "en") == "Hello"
    assert translate_if_needed("Hello", "fr") == "Hello"

@patch("deep_translator.GoogleTranslator")
def test_translate_if_needed_es_success(mock_translator):
    mock_instance = mock_translator.return_value
    mock_instance.translate.return_value = "Hola"

    result = translate_if_needed("Hello", "es")

    assert result == "Hola"
    mock_translator.assert_called_once_with(source="en", target="es")
    mock_instance.translate.assert_called_once_with("Hello")

@patch("deep_translator.GoogleTranslator")
def test_translate_if_needed_es_exception(mock_translator):
    mock_instance = mock_translator.return_value
    mock_instance.translate.side_effect = Exception("API Error")

    result = translate_if_needed("Hello", "es")

    assert result == "Hello"
    mock_translator.assert_called_once_with(source="en", target="es")
    mock_instance.translate.assert_called_once_with("Hello")
