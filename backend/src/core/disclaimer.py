DISCLAIMER_EN = (
    "IMPORTANT: This is not legal advice. LegalClear is an "
    "AI-powered tool that helps you understand legal documents "
    "in plain language. It does not create an attorney-client "
    "relationship and is not a substitute for advice from a "
    "licensed attorney. For decisions involving your legal "
    "rights, obligations, or significant financial "
    "consequences, consult a licensed attorney in your "
    "jurisdiction."
)

DISCLAIMER_ES = (
    "IMPORTANTE: Esto no es asesoramiento legal. LegalClear "
    "es una herramienta de inteligencia artificial que le "
    "ayuda a comprender documentos legales en lenguaje "
    "sencillo. No crea una relacion abogado-cliente y no "
    "sustituye el consejo de un abogado con licencia. Para "
    "decisiones que involucren sus derechos legales, consulte "
    "a un abogado con licencia en su jurisdiccion."
)

SHORT_DISCLAIMER_EN = (
    "Not legal advice. For informational purposes only."
)

SHORT_DISCLAIMER_ES = (
    "No es asesoramiento legal. "
    "Solo para fines informativos."
)

CRIMINAL_WARNING_EN = (
    "This appears to be a criminal matter. LegalClear can "
    "help you understand what this document says in plain "
    "language. However, criminal cases involve rights that "
    "can be permanently affected by your decisions. If you "
    "cannot afford an attorney, you have the right to a "
    "public defender. Contact your local public defender "
    "before making any decisions about your case."
)

CRIMINAL_WARNING_ES = (
    "Este parece ser un asunto penal. LegalClear puede "
    "ayudarle a comprender este documento en lenguaje "
    "sencillo. Sin embargo, los casos penales involucran "
    "derechos que pueden verse afectados permanentemente. "
    "Si no puede pagar un abogado, tiene derecho a un "
    "defensor publico. Comuniquese con el defensor publico "
    "local antes de tomar decisiones sobre su caso."
)

PLEA_WARNING_EN = (
    "WARNING: This is a plea agreement. Signing this "
    "document waives important legal rights that cannot "
    "be recovered. Do NOT sign without first speaking to "
    "an attorney or public defender. This is the single "
    "most important action you can take right now."
)

PLEA_WARNING_ES = (
    "ADVERTENCIA: Este es un acuerdo de culpabilidad. "
    "Firmar este documento renuncia a derechos legales "
    "importantes que no se pueden recuperar. NO firme sin "
    "antes hablar con un abogado o defensor publico."
)


def get_disclaimer(lang: str,
                   level: str = "standard") -> str:
    lang = "es" if lang == "es" else "en"
    if level == "standard":
        return DISCLAIMER_ES if lang == "es" else DISCLAIMER_EN
    if level == "short":
        return (SHORT_DISCLAIMER_ES
                if lang == "es" else SHORT_DISCLAIMER_EN)
    if level == "criminal":
        return (CRIMINAL_WARNING_ES
                if lang == "es" else CRIMINAL_WARNING_EN)
    if level == "plea":
        return (PLEA_WARNING_ES
                if lang == "es" else PLEA_WARNING_EN)
    return DISCLAIMER_EN
