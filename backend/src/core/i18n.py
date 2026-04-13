from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = ['en', 'es']

def get_lang(detected: str, user_preference: str = None) -> str:
    if user_preference in SUPPORTED_LANGUAGES:
        return user_preference
    if detected in SUPPORTED_LANGUAGES:
        return detected
    return 'en'

def translate_if_needed(text: str, target_lang: str) -> str:
    if target_lang == 'en':
        return text
    if target_lang == 'es':
        try:
            return GoogleTranslator(source='en', target='es').translate(text)
        except Exception:
            return text
    return text
