import json
import anthropic
from src.core.config import settings

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

class ClassifierAgent:
    def __init__(self):
        self.model = "claude-3-5-haiku-20241022"
        self.system_prompt = (
            "You are a legal document classification expert. "
            "Your only job is to analyze legal documents and return "
            "precise structured metadata about what they are. "
            "You are highly accurate. You never guess. "
            "If uncertain about any field, return 'unknown'. "
            "You always return valid JSON and nothing else. "
            "No preamble. No explanation. No markdown. JSON only."
        )

    def get_price_tier(self, document: dict) -> dict:
        tokens = document.get('token_estimate', 0)
        if tokens < 4000:
            return {'tier': 'small', 'price_usd': 5, 'label': 'Short document (under 5 pages)'}
        elif tokens < 12000:
            return {'tier': 'medium', 'price_usd': 10, 'label': 'Standard document (5-15 pages)'}
        else:
            return {'tier': 'large', 'price_usd': 15, 'label': 'Complex document (15+ pages)'}

    async def classify(self, document: dict) -> dict:
        text = document.get('text', '')
        # Truncate to approx ~6000 tokens naively by length, ignoring true tokenization for now
        trunc_text = text[:24000]

        user_prompt = f"""
Analyze this document and return JSON with exactly these fields:
- document_category: str (one of: contract, government_form, court_filing, notice, agreement, will_estate, employment, real_estate, financial, criminal_charge, criminal_summons, plea_agreement, restraining_order, expungement_petition, small_claims_complaint, small_claims_response, small_claims_judgment, other)
- document_type: str
- jurisdiction_type: str (federal, state, local, unknown)
- jurisdiction_name: str
- issuing_agency: str
- parties: list[str] (max 4)
- key_dates: list[dict] (each: {{label, date, importance}})
- filing_deadline: str ("Date string", "none", or "unknown")
- estimated_complexity: str (simple, moderate, complex)
- detected_language: str (en, es, unknown)
- red_flag_preview: list[str] (up to 3 brief concerns)
- confidence: float (0.0 to 1.0)

Document text:
{trunc_text}
"""
        
        fallback = {
            "document_category": "unknown",
            "jurisdiction_name": "unknown",
            "confidence": 0.0
        }

        if not settings.ANTHROPIC_API_KEY:
            # Without API Key during scaffold, return mock
            return {
                "document_category": "contract",
                "jurisdiction_name": "Florida",
                "confidence": 0.9,
                "detected_language": "en"
            }

        try:
            response = await client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=[
                    {
                        "type": "text", 
                        "text": self.system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[{"role": "user", "content": user_prompt}]
            )
            raw = response.content[0].text
            return json.loads(raw)
        except Exception:
            try:
                # retry
                response = await client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=[{"type": "text", "text": self.system_prompt + " STRICT JSON ONLY."}],
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return json.loads(response.content[0].text)
            except Exception:
                return fallback
