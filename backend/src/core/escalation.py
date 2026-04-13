import json
from pathlib import Path
from .disclaimer import get_disclaimer

class EscalationRouter:
    def __init__(self):
        data_path = Path(__file__).resolve().parent.parent / 'data' / 'jurisdictions.json'
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.jurisdictions = json.load(f)
        except Exception:
            self.jurisdictions = {}

    def route(self, classification: dict, lang: str = 'en') -> dict:
        cat = classification.get('document_category', 'other')
        
        green_cats = ['contract', 'agreement', 'real_estate', 'employment', 'financial', 'will_estate', 'other']
        yellow_cats = ['government_form', 'court_filing', 'small_claims_complaint', 'small_claims_response', 'small_claims_judgment', 'expungement_petition']
        red_criminal_cats = ['criminal_charge', 'criminal_summons', 'restraining_order']
        red_plea_cats = ['plea_agreement']

        res = {
            "disclaimer_level": "standard",
            "show_attorney_warning": False,
            "show_public_defender_info": False,
            "pre_analysis_warning": None,
            "escalation_color": "green",
            "resource_links": [
                {"name": "Free legal aid", "url": "https://www.lawhelp.org"},
                {"name": "Public Defender Search", "url": "https://www.nacdl.org/Landing/PublicDefenders"},
                {"name": "Court Self-Help", "url": "https://www.ncsc.org/topics/access-and-fairness/self-represented-litigants/resource-guide"}
            ]
        }

        if cat in green_cats:
            pass
        elif cat in yellow_cats:
            res['escalation_color'] = 'yellow'
            res['show_attorney_warning'] = True
        elif cat in red_criminal_cats:
            res['disclaimer_level'] = 'criminal'
            res['escalation_color'] = 'red'
            res['show_attorney_warning'] = True
            res['show_public_defender_info'] = True
            res['pre_analysis_warning'] = get_disclaimer(lang, 'criminal')
        elif cat in red_plea_cats:
            res['disclaimer_level'] = 'plea'
            res['escalation_color'] = 'red'
            res['show_attorney_warning'] = True
            res['show_public_defender_info'] = True
            res['pre_analysis_warning'] = get_disclaimer(lang, 'plea')

        jur = classification.get('jurisdiction_name')
        if jur and jur in self.jurisdictions:
            j_data = self.jurisdictions[jur]
            if j_data.get('legal_aid_url'):
                res['resource_links'].append({"name": f"{jur} Legal Aid", "url": j_data['legal_aid_url']})
            if j_data.get('public_defender_url') and res['show_public_defender_info']:
                res['resource_links'].append({"name": f"{jur} Public Defender", "url": j_data['public_defender_url']})

        return res
