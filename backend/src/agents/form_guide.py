import json
import anthropic
from src.core.config import settings
from src.core.disclaimer import get_disclaimer

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

class FormGuideAgent:
    def __init__(self):
        self.model = "claude-sonnet-4-6"
        self.system_prompt = (
            "You are a government and court form completion guide for LegalClear. "
            "You help ordinary people fill out legal and government forms correctly "
            "and completely. You explain each field in plain language. You know "
            "requirements for federal and state forms across the US. You flag common "
            "mistakes. You tell people exactly what to write. You never give legal advice. "
            "When the user's language is Spanish, respond entirely in Spanish. "
            "Return valid JSON only. No preamble. No markdown. JSON only."
        )

    async def guide(self, document: dict, classification: dict, lang: str = 'en') -> dict:
        doc_cat = classification.get('document_category', '')
        if doc_cat not in ['government_form', 'court_filing', 'small_claims_complaint', 'small_claims_response', 'small_claims_judgment']:
            return {}

        lang_instr = "Respond entirely in Spanish." if lang == 'es' else ""
        text = document.get('text', '')[:40000]

        user_prompt = f"""
{lang_instr}
Form extracted text: {text}

Return JSON with these fields:
- form_overview: str
- before_you_start: list[str]
- sections: list[dict] (each: {{section_name, description, fields: list[{{field_name, field_number, plain_label, instructions, example, common_mistakes, required: bool}}]}})
- where_to_file: dict ({{methods, address, online_url, fee, copies_needed, what_to_keep}})
- after_filing: list[str]
- deadline_warning: str or null
- small_claims_hearing_tips: list[str] or null
- disclaimer: str
"""
        res = {
            "form_overview": "Mock form guide",
            "sections": [],
            "where_to_file": {},
        }

        if settings.ANTHROPIC_API_KEY:
            try:
                response = await client.messages.create(
                    model=self.model,
                    max_tokens=2500,
                    system=[{"type": "text", "text": self.system_prompt, "cache_control": {"type": "ephemeral"}}],
                    messages=[{"role": "user", "content": user_prompt}]
                )
                res = json.loads(response.content[0].text)
            except Exception:
                pass

        res['disclaimer'] = get_disclaimer(lang, 'standard')
        return res

    async def answer_form_question(self, document: dict, classification: dict, guide: dict, question: str, chat_history: list, lang: str = 'en') -> dict:
        return {
            "answer": f"Mock form guide answer to: {question}",
            "confidence": "high",
            "disclaimer": get_disclaimer(lang, 'short'),
            "language": lang
        }
