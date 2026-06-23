import json
from src.core.disclaimer import get_disclaimer


class BaseAgent:
    async def _get_anthropic_json(self, model: str, system_prompt: str, user_prompt: str, lang: str = "en", max_tokens: int = 4096) -> dict:
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=[{
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }],
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )
            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            result = json.loads(raw)
            result["disclaimer"] = get_disclaimer(lang, "standard")
            return result
        except Exception as e:
            return {"error": True, "message": str(e),
                    "disclaimer": get_disclaimer(lang, "standard")}
