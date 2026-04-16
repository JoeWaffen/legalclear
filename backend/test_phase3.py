import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.classifier import ClassifierAgent

lease_doc = {
    "text": (
        "RESIDENTIAL LEASE AGREEMENT "
        "This lease is between Landlord Robert Johnson and "
        "Tenant Sarah Williams for 456 Oak St Miami FL 33101. "
        "Monthly rent $2200 due on the 1st. Late fee $200 "
        "after 5 days. Term 12 months starting March 1 2026. "
        "AUTO-RENEWAL: Lease renews automatically unless 60 "
        "days notice given. ARBITRATION: All disputes subject "
        "to binding arbitration, tenant waives jury trial."
    ),
    "token_estimate": 500,
    "language": "en"
}

criminal_doc = {
    "text": (
        "STATE OF FLORIDA vs DEFENDANT "
        "CRIMINAL COMPLAINT MISDEMEANOR "
        "You are hereby charged with Petit Theft First Degree "
        "Misdemeanor Florida Statute 812.014. "
        "Date of alleged offense February 10 2026. "
        "You must appear before Judge Martinez at Broward "
        "County Courthouse Room 4B on March 15 2026 at 9AM. "
        "Failure to appear will result in a warrant."
    ),
    "token_estimate": 300,
    "language": "en"
}

small_claims_doc = {
    "text": (
        "SMALL CLAIMS COURT COMPLAINT "
        "Plaintiff Maria Gonzalez 789 Palm Ave Stuart FL 34994 "
        "Defendant Quick Fix Contractors LLC 321 US-1 Stuart FL "
        "Amount claimed $3500.00 "
        "Reason Contractor accepted payment for roof repair work "
        "completed January 2026. Work was defective and caused "
        "water damage. Contractor refused to remedy."
    ),
    "token_estimate": 300,
    "language": "en"
}

async def run():
    agent = ClassifierAgent()

    print("Classifying lease...")
    lease = await agent.classify(lease_doc)
    print(f"  category: {lease['document_category']}")
    print(f"  confidence: {lease['confidence']}")
    assert lease["document_category"] in [
        "real_estate", "contract", "agreement"], (
        f"Lease wrong category: {lease['document_category']}")

    print("Classifying criminal document...")
    crim = await agent.classify(criminal_doc)
    print(f"  category: {crim['document_category']}")
    assert crim["document_category"] in [
        "criminal_charge", "criminal_summons"], (
        f"Criminal wrong: {crim['document_category']}")

    print("Classifying small claims...")
    sc = await agent.classify(small_claims_doc)
    print(f"  category: {sc['document_category']}")
    assert "small_claims" in sc["document_category"] or \
           sc["document_category"] == "court_filing", (
        f"Small claims wrong: {sc['document_category']}")

    tier = agent.get_price_tier({"token_estimate": 500})
    assert tier["tier"] == "small"
    tier2 = agent.get_price_tier({"token_estimate": 8000})
    assert tier2["tier"] == "medium"
    tier3 = agent.get_price_tier({"token_estimate": 20000})
    assert tier3["tier"] == "large"
    print("Price tiers OK")

    print("\nALL PHASE 3 ASSERTIONS PASSED")

asyncio.run(run())
