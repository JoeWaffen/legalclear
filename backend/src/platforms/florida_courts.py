import json
from pathlib import Path

class PDFAGenerator:
    def __init__(self):
        pass

    def generate_complaint(self, case_data: dict, output_path: str) -> str:
        # Mocked generation (would use reportlab/weasyprint)
        with open(output_path + '_complaint.pdf', 'w') as f:
            f.write("Mock PDF/A Complaint for " + case_data.get('plaintiff_name', ''))
        return output_path + '_complaint.pdf'

    def generate_civil_cover_sheet(self, case_data: dict, output_path: str) -> str:
        with open(output_path + '_cover.pdf', 'w') as f:
            f.write("Mock PDF/A Civil Cover Sheet")
        return output_path + '_cover.pdf'

    def generate_summons(self, case_data: dict, output_path: str) -> str:
        with open(output_path + '_summons.pdf', 'w') as f:
            f.write("Mock PDF/A Summons")
        return output_path + '_summons.pdf'

    def generate_packet(self, case_data: dict, output_dir: str) -> dict:
        import os
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.join(output_dir, 'packet')
        return {
            "complaint_path": self.generate_complaint(case_data, base),
            "cover_sheet_path": self.generate_civil_cover_sheet(case_data, base),
            "summons_path": self.generate_summons(case_data, base),
            "packet_dir": output_dir,
            "county": case_data.get('county', 'Unknown'),
            "court_name": case_data.get('court_name', 'Unknown Court'),
            "filing_fee_estimate": "$55 - $300"
        }

class CountyRouter:
    def __init__(self):
        data_path = Path(__file__).resolve().parent.parent / 'data' / 'jurisdictions.json'
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.jurisdictions = json.load(f)
        except Exception:
            self.jurisdictions = {}

    def route(self, county: str) -> dict:
        return {
            "county": county,
            "court_name": f"{county} County Court",
            "portal_county_code": "01",
            "clerk_address": "100 Courthouse Sq",
            "filing_fee_small_claims": "$55.00",
            "portal_url": "https://www.myflcourtaccess.com",
            "self_help_url": "https://help.flcourts.gov"
        }

    def detect_county_from_address(self, address: str) -> str:
        if "Martin" in address: return "Martin"
        return "Unknown"

    def get_deep_link(self, county: str) -> str:
        return "https://www.myflcourtaccess.com/login"

class FloridarCourtsConnector:
    # MODE B — requires portal credentials
    def __init__(self):
        pass

    async def login(self, email, password) -> bool:
        return True

    async def file_packet(self, complaint_path, cover_sheet_path, summons_path, county, case_type='small_claims') -> dict:
        return {"success": True, "case_number": "2026-SC-001", "confirmation": "MOCK_CONF", "status": "filed"}

    async def check_status(self, case_number: str) -> dict:
        return {"status": "accepted"}

class ManualFilingHelper:
    @staticmethod
    def get_instructions(county: str, lang: str = 'en') -> dict:
        en_steps = [
            "1. Go to myflcourtaccess.com, create free account.",
            "2. Click E-File in top navigation.",
            f"3. Select your county: {county}.",
            "4. Select: County Civil -> Small Claims.",
            "5. Upload documents in this order: Document 1: Civil Cover Sheet (Form 1.997), Document 2: Complaint (Form 7B), Document 3: Summons",
            "6. Pay the filing fee.",
            "7. Submit. Receive email confirmation with case number within 1-2 business days.",
            "8. Save your case number to track status."
        ]
        return {
            "steps": en_steps, # (mocking translation)
            "portal_url": "https://myflcourtaccess.com",
            "deep_link": "https://myflcourtaccess.com",
            "county": county,
            "documents_to_upload": ["Cover Sheet", "Complaint", "Summons"],
            "filing_fee": "$55-$300",
            "tips": "Double check PDF/A formats.",
            "disclaimer": "LegalClear prepares your documents. You submit them. We are not affiliated with MyFLCourtAccess."
        }

    @staticmethod
    def get_deep_link_button(county: str) -> dict:
        return {
            "label_en": "File on MyFLCourtAccess",
            "label_es": "Presentar en MyFLCourtAccess",
            "url": "https://myflcourtaccess.com",
            "note_en": "Opens the official Florida state portal in a new tab.",
            "note_es": "Abre el portal oficial de Florida en una nueva pestaña."
        }
