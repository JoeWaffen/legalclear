import re

class TextCleaner:
    def __init__(self):
        pass
        
    def clean(self, raw_text: str) -> str:
        text = re.sub(r'[\x00]', '', raw_text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]{2,}', ' ', text)
        return text.strip()

    def detect_language(self, text: str) -> str:
        text_lower = text.lower()
        spanish_words = ['contrato', 'acuerdo', 'demanda', 'tribunal', 'firmante', 'arrendamiento']
        english_words = ['agreement', 'contract', 'plaintiff', 'defendant', 'lease', 'hereby']
        
        es_count = sum(text_lower.count(w) for w in spanish_words)
        en_count = sum(text_lower.count(w) for w in english_words)
        
        if es_count > en_count:
            return 'es'
        return 'en'

    def truncate_for_llm(self, text: str, max_tokens: int = 90000) -> str:
        approx_tokens = int(len(text.split()) * 1.3)
        if approx_tokens <= max_tokens:
            return text
            
        words = text.split()
        keep_total = int(max_tokens / 1.3)
        first_part_len = int(keep_total * 0.6)
        last_part_len = int(keep_total * 0.4)
        
        truncated = words[:first_part_len] + ["[Document truncated for processing]"] + words[-last_part_len:]
        return " ".join(truncated)
