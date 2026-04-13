import json
import anthropic
from src.core.config import settings
from src.core.disclaimer import get_disclaimer

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

class RiskScannerAgent:
    def __init__(self):
        self.model = "claude-haiku-4-5-20251001"
        self.system_prompt = (
            "You are a legal document risk scanner for LegalClear. "
            "You identify clauses and terms that are unusual, potentially harmful, "
            "one-sided, or worth attention. You score risk clearly using RED, YELLOW, GREEN. "
            "You explain why each item matters in plain language a non-lawyer can understand. "
            "You are thorough, direct, and never alarmist. "
            "When the user's language is Spanish, respond entirely in Spanish. "
            "Return valid JSON only. No preamble. No markdown. JSON only."
        )

    async def scan(self, document: dict, classification: dict, lang: str = 'en') -> dict:
        text = document.get('text', '')[:24000]
        lang_instr = "Respond entirely in Spanish." if lang == 'es' else ""

        user_prompt = f"""
{lang_instr}
Document text: {text}

Return JSON with these fields:
- overall_risk_level: str (LOW / MEDIUM / HIGH)
- risk_summary: str (2-3 sentence assessment)
- clauses: list[dict] (each: {{clause_title, risk_level (RED/YELLOW/GREEN), what_it_says, why_it_matters, what_to_do, quote (max 100 chars)}})
- missing_protections: list[dict] (each: {{protection_name, why_important, what_to_ask_for}})
- red_count: int
- yellow_count: int
- green_count: int
- top_concerns: list[str] (top 3, in order)
- negotiation_tips: list[str]
- disclaimer: str
"""
        res = {
            "overall_risk_level": "LOW",
            "risk_summary": "Mock risk scan.",
            "clauses": [],
            "missing_protections": [],
            "red_count": 0, "yellow_count": 0, "green_count": 0,
            "top_concerns": [],
            "negotiation_tips": []
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
        return res
