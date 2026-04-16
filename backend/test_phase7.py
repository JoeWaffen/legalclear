import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.expungement import ExpungementAgent

expungement_text = """
PETITION FOR EXPUNGEMENT OF CRIMINAL RECORD
Petitioner: James Robert Williams
Case Number: 2019-MM-014521-A
Court: Palm Beach County Court
Offense: Misdemeanor Petit Theft First Offense
Florida Statute 812.014(2)(e)
Date of Offense: August 3 2019
Disposition: Guilty Plea Probation 12 months
Probation Completed: August 3 2020
All fines paid: Yes
Adjudication withheld: Yes
"""

document = {"text": expungement_text, "language": "en"}
classification = {
    "document_category": "expungement_petition",
    "document_type": "expungement_petition_florida",
    "jurisdiction_name": "Florida",
    "estimated_complexity": "moderate"
}

async def run():
    agent = ExpungementAgent()

    guide = await agent.guide(document, classification, "en")
    assert not guide.get("error"), (
        f"Guide error: {guide.get('message')}")
    assert "what_is_expungement" in guide
    assert "steps" in guide
    assert "what_changes_after" in guide
    assert "disclaimer" in guide
    print(f"Steps count: {len(guide.get('steps', []))}")
    print(f"Changes: "
          f"{guide.get('what_changes_after', ['none'])[0]}")

    elig = await agent.check_eligibility(
        "Florida", "misdemeanor petit theft first offense",
        6, "en")
    assert "likely_eligible" in elig
    assert "confidence" in elig
    assert "reasoning" in elig
    print(f"Eligible: {elig['likely_eligible']} "
          f"Confidence: {elig['confidence']}")
    print(f"Reasoning: {elig['reasoning'][:150]}")

    elig_es = await agent.check_eligibility(
        "Florida", "misdemeanor petit theft", 6, "es")
    assert "likely_eligible" in elig_es
    print(f"ES reasoning: "
          f"{elig_es.get('reasoning', '')[:100]}")

    print("\nALL PHASE 7 ASSERTIONS PASSED")

asyncio.run(run())
