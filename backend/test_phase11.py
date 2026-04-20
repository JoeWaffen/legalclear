import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.platforms.florida_courts import (
    PDFAGenerator, CountyRouter, ManualFilingHelper)

case_data = {
    "plaintiff_name": "Maria Garcia",
    "plaintiff_address": "123 Main St",
    "plaintiff_city_state_zip": "Stuart FL 34994",
    "plaintiff_phone": "772-555-0100",
    "defendant_name": "ABC Landlord LLC",
    "defendant_address": "456 Oak Ave",
    "defendant_city_state_zip": "Stuart FL 34994",
    "amount_claimed": 2500.00,
    "claim_reason": (
        "Security deposit not returned after "
        "move-out on January 15 2026."),
    "incident_date": "2026-01-15",
    "county": "Martin",
    "court_name": "Martin County Court"
}

def test():
    gen = PDFAGenerator()
    packet = gen.generate_packet(
        case_data, "/tmp/lc_test_packet/")

    for key in ["complaint_path",
                "cover_sheet_path",
                "summons_path"]:
        path = packet[key]
        assert os.path.exists(path), (
            f"File not found: {path}")
        size = os.path.getsize(path)
        assert size > 0, f"Empty file: {path}"
        print(f"{key}: {round(size/1024,1)}KB OK")

    router = CountyRouter()
    info = router.route("Martin")
    assert "court_name" in info
    assert "portal_url" in info
    assert "martin" in info["portal_url"].lower() or \
           "myflcourtaccess" in info["portal_url"].lower()
    print(f"County route: {info['portal_url']}")

    helper = ManualFilingHelper()
    instr_en = helper.get_instructions("Martin", "en")
    assert "steps" in instr_en
    assert len(instr_en["steps"]) >= 5
    assert "disclaimer" in instr_en
    print(f"EN steps: {len(instr_en['steps'])}")

    instr_es = helper.get_instructions("Martin", "es")
    assert "steps" in instr_es
    print(f"ES steps[0]: {instr_es['steps'][0][:60]}")

    btn = helper.get_deep_link_button("Martin")
    assert "url" in btn
    assert "label_en" in btn
    assert "label_es" in btn
    print(f"Button URL: {btn['url']}")

    print("\nALL PHASE 11 ASSERTIONS PASSED")

test()
