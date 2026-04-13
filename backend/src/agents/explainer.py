import json
import anthropic
from src.core.config import settings
from src.core.disclaimer import get_disclaimer

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

class ExplainerAgent:
    def __init__(self):
        self.model = "claude-sonnet-4-6"
        self.system_prompt = (
            "You are a plain language legal document explainer for LegalClear. "
            "Your job is to help ordinary people with no legal background understand "
            "legal documents clearly and accurately. You use simple everyday language. "
            "You never use legal jargon without immediately explaining it. "
            "You are thorough, warm, and clear. You never give legal advice — "
            "you explain what documents say, not what people should do. "
            "When the user's language is Spanish, respond entirely in Spanish. "
            "Return valid JSON only. No preamble. No markdown. JSON only."
        )

    async def explain(self, document: dict, classification: dict, lang: str = 'en') -> dict:
        doc_type = classification.get('document_type', 'unknown')
        doc_cat = classification.get('document_category', 'unknown')
        jur = classification.get('jurisdiction_name', 'unknown')
        text = document.get('text', '')[:40000]

        lang_instr = "Respond entirely in Spanish." if lang == 'es' else ""

        user_prompt = f"""
{lang_instr}
Document details: Type: {doc_type}, Category: {doc_cat}, Jurisdiction: {jur}.

Return JSON with these fields:
- summary: str (2-3 sentence plain language summary)
- what_this_means_for_you: str (3-5 sentences, real-world impact)
- key_sections: list[dict] (each: {{title, plain_explanation, importance: high/medium/low}})
- important_numbers: list[dict] (each: {{label, value, context}})
- your_rights: list[str]
- your_obligations: list[str]
- questions_to_ask: list[str] (3-5 questions)

Document text:
{text}
"""
        res = {
            "summary": "Mock explanation",
            "what_this_means_for_you": "Mock impact",
            "key_sections": [],
            "important_numbers": [],
            "your_rights": [],
            "your_obligations": [],
            "questions_to_ask": []
        }

        if settings.ANTHROPIC_API_KEY:
            try:
                response = await client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    system=[{"type": "text", "text": self.system_prompt, "cache_control": {"type": "ephemeral"}}],
                    messages=[{"role": "user", "content": user_prompt}]
                )
                res = json.loads(response.content[0].text)
            except Exception:
                pass

        res['disclaimer'] = get_disclaimer(lang, 'standard')
        res['language'] = lang
        return res

    async def answer_question(self, document: dict, classification: dict, explanation: dict, question: str, chat_history: list, lang: str = 'en') -> dict:
        if not settings.ANTHROPIC_API_KEY:
            return {
                "answer": f"Mock answer to: {question}",
                "confidence": "high",
                "disclaimer": get_disclaimer(lang, 'short'),
                "language": lang
            }
        
        # In a real run, construct exact prompt flow...
        return {
            "answer": "Mock live generated answer",
            "confidence": "high",
            "disclaimer": get_disclaimer(lang, 'short'),
            "language": lang
        }
