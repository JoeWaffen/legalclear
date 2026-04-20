import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.risk_scanner import RiskScannerAgent

risky_contract = """
COMMERCIAL LEASE AGREEMENT

AUTO-RENEWAL CLAUSE: This lease automatically renews for
one-year terms without any notice required from either party.

BINDING ARBITRATION: Tenant permanently and irrevocably
waives the right to a jury trial. All disputes must be
resolved through binding arbitration selected solely by
Landlord.

TERMINATION: Landlord may terminate this lease at any time
for any reason with 3 days notice. Tenant may only terminate
with 90 days written notice.

PERSONAL GUARANTEE: Tenant personally guarantees all
obligations under this lease including amounts owed by any
business entity.

RENT INCREASES: Landlord may increase rent at any time with
7 days notice.

INSPECTION: Landlord may enter the premises at any time
without notice for any reason.
"""

document = {"text": risky_contract, "language": "en"}
classification = {
    "document_category": "contract",
    "document_type": "commercial_lease",
    "jurisdiction_name": "Florida",
    "estimated_complexity": "moderate"
}

async def run():
    agent = RiskScannerAgent()
    result = await agent.scan(document, classification, "en")

    assert not result.get("error"), (
        f"Scanner error: {result.get('message')}")
    assert "overall_risk_level" in result
    assert "clauses" in result
    assert "red_count" in result
    assert "disclaimer" in result

    print(f"Overall risk: {result['overall_risk_level']}")
    print(f"Red: {result['red_count']} "
    f"Yellow: {result['yellow_count']} "
    f"Green: {result['green_count']}")
    
    for c in result.get("clauses", []):
        print(f"  {c['risk_level']}: {c['clause_title']}")

    assert result["overall_risk_level"] == "HIGH", (
        f"Expected HIGH got {result['overall_risk_level']}")
    assert result["red_count"] >= 2, (
        f"Expected >= 2 red, got {result['red_count']}")
    assert len(result.get("missing_protections", [])) >= 1

    print("\nALL PHASE 6 ASSERTIONS PASSED")

asyncio.run(run())
