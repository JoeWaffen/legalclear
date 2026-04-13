DISCLAIMER_EN = "This is not legal advice. No attorney-client relationship is created. Please consult a licensed attorney in your jurisdiction for legal advice tailored to your situation."
DISCLAIMER_ES = "Esto no es asesoramiento legal. No se crea una relación abogado-cliente. Por favor consulte a un abogado con licencia en su jurisdicción."

SHORT_DISCLAIMER_EN = "Not legal advice. For informational purposes only."
SHORT_DISCLAIMER_ES = "No es asesoramiento legal. Solo para fines informativos."

CRIMINAL_WARNING_EN = "WARNING: This appears to be a criminal matter. Your rights can be permanently affected. Please contact a public defender or private attorney immediately before making decisions."
CRIMINAL_WARNING_ES = "ADVERTENCIA: Este parece ser un asunto penal. Sus derechos pueden verse afectados permanentemente. Comuníquese con un defensor público o abogado privado inmediatamente."

PLEA_WARNING_EN = "STRONG WARNING: Do not sign a plea agreement without speaking to an attorney or public defender first. This waives extremely important constitutional rights."
PLEA_WARNING_ES = "FUERTE ADVERTENCIA: No firme un acuerdo de culpabilidad sin hablar antes con un abogado. Esto renuncia a derechos constitucionales importantes."

def get_disclaimer(lang: str, level: str = 'standard') -> str:
    lang = 'es' if lang == 'es' else 'en'
    
    if level == 'short':
        return SHORT_DISCLAIMER_ES if lang == 'es' else SHORT_DISCLAIMER_EN
    elif level == 'criminal':
        return CRIMINAL_WARNING_ES if lang == 'es' else CRIMINAL_WARNING_EN
    elif level == 'plea':
        return PLEA_WARNING_ES if lang == 'es' else PLEA_WARNING_EN
    else:
        return DISCLAIMER_ES if lang == 'es' else DISCLAIMER_EN
