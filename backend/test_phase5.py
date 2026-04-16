import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.form_guide import FormGuideAgent

small_claims_text = """
SMALL CLAIMS COURT COMPLAINT FORM
Martin County Court Stuart Florida
Case Number: _______________
Plaintiff Full Legal Name: _______________
Plaintiff Street Address: _______________
Plaintiff City State Zip: _______________
Plaintiff Phone: _______________
Defendant Full Legal Name or Business: _______________
Defendant Address: _______________
Amount Claimed max 8000: $_______________
Date of Incident: _______________
Description of Claim: _______________
Plaintiff Signature: _______________ Date: ______
"""

document = {"text": small_claims_text, "language": "en"}
classification = {
    "document_category": "small_claims_complaint",
    "document_type": "small_claims_complaint_florida",
    "jurisdiction_name": "Florida",
    "issuing_agency": "Martin County Court",
    "filing_deadline": "unknown",
    "estimated_complexity": "simple"
}

async def run():
    agent = FormGuideAgent()

    guide = await agent.guide(document, classification, "en")
    assert not guide.get("error"), (
        f"Guide error: {guide.get('message')}")
    assert "form_overview" in guide
    assert "sections" in guide
    assert "where_to_file" in guide
    assert "disclaimer" in guide
    print(f"Form overview: {guide['form_overview'][:150]}")
    print(f"Sections count: {len(guide.get('sections', []))}")

    qa = await agent.answer_form_question(
        document, classification, guide,
        "Where do I file this form and how much does it cost?",
        [], "en")
    assert "answer" in qa
    assert len(qa["answer"]) > 20
    print(f"Q&A: {qa['answer'][:150]}")

    print("\nALL PHASE 5 ASSERTIONS PASSED")

asyncio.run(run())
