import json
import anthropic
from src.core.config import settings
from src.core.disclaimer import get_disclaimer

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

class ExpungementAgent:
    def __init__(self):
        self.model = "claude-sonnet-4-6"
        self.haiku = "claude-haiku-4-5-20251001"
        self.system_prompt = (
            "You are an expungement petition guide for LegalClear. "
            "You help people understand the expungement process and fill out "
            "expungement petitions correctly. Expungement seals or clears a criminal record, "
            "giving people a fresh start in employment, housing, and licensing. "
            "You explain every step clearly in plain language. You know expungement laws "
            "for all 50 US states. You never give legal advice. "
            "When the user's language is Spanish, respond entirely in Spanish. "
            "Return valid JSON only. No preamble. No markdown. JSON only."
        )

    async def guide(self, document: dict, classification: dict, lang: str = 'en') -> dict:
        doc_cat = classification.get('document_category', '')
        if doc_cat != 'expungement_petition':
            return {}

        text = document.get('text', '')[:40000]
        lang_instr = "Respond entirely in Spanish." if lang == 'es' else ""

        user_prompt = f"""
{lang_instr}
Document text: {text}

Return JSON with these fields:
- what_is_expungement: str
- eligibility_overview: str
- before_you_start: list[str]
- steps: list[dict] (each: {{step_number, title, instructions, tips, estimated_time, cost}})
- form_fields: list[dict] (each: {{field_name, plain_label, instructions, example, common_mistakes, required: bool}})
- where_to_file: dict ({{court_type, methods, address_note, online_url, fee, fee_waiver_note}})
- after_filing: list[str]
- what_changes_after: list[str]
- what_does_not_change: list[str]
- free_resources: list[dict] (each: {{label, url, description}})
- disclaimer: str
"""
        res = {
            "what_is_expungement": "Mock expungement guide.",
            "free_resources": [
                {"label": "Expungement Info", "url": "https://www.expungement.com", "description": "National context"}
            ]
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

    async def check_eligibility(self, jurisdiction: str, offense_description: str, years_since_offense: int, lang: str = 'en') -> dict:
        lang_instr = "Respond entirely in Spanish." if lang == 'es' else ""
        user_prompt = f"""
{lang_instr}
Jurisdiction: {jurisdiction}
Offense: {offense_description}
Years since: {years_since_offense}

Return JSON:
- likely_eligible: bool
- confidence: str
- reasoning: str
- key_factors: list[str]
- next_steps: list[str]
- disclaimer: str
"""
        res = {
            "likely_eligible": False,
            "confidence": "low",
            "reasoning": "Mock eligibility.",
            "key_factors": [],
            "next_steps": []
        }

        if settings.ANTHROPIC_API_KEY:
             try:
                 response = await client.messages.create(
                     model=self.haiku,
                     max_tokens=1000,
                     system=[{"type": "text", "text": self.system_prompt}],
                     messages=[{"role": "user", "content": user_prompt}]
                 )
                 res = json.loads(response.content[0].text)
             except Exception:
                 pass
        
        res['disclaimer'] = get_disclaimer(lang, 'standard')
        return res
