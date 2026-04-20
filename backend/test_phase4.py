import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ingestion import ingest_document
from src.agents.classifier import ClassifierAgent
from src.agents.explainer import ExplainerAgent

async def run():
    classifier = ClassifierAgent()
    explainer = ExplainerAgent()

    with open("test_lease.txt", "wb") as f:
        f.write(b"RESIDENTIAL LEASE AGREEMENT. This lease is between Landlord and Tenant for 123 Main St. Rent is 1000 due on the 1st of every month. Tenant handles utilities. Landlord handles repairs.")

    with open("test_lease.txt", "rb") as f:
        data = f.read()

    doc = await ingest_document(data, "test_lease.txt")
    assert not doc.get("error")

    classification = await classifier.classify(doc)
    print(f"Category: {classification['document_category']}")

    explanation = await explainer.explain(
        doc, classification, "en")

    assert not explanation.get("error"), (
        f"Explainer error: {explanation.get('message')}")
    assert "summary" in explanation
    assert "your_rights" in explanation
    assert "disclaimer" in explanation
    assert explanation["language"] == "en"

    print(f"Summary: {explanation['summary'][:150]}")
    print(f"Rights count: {len(explanation.get('your_rights',[]))}")

    qa = await explainer.answer_question(
        doc, classification, explanation,
        "What happens if I pay my rent late?",
        [], "en")
    assert "answer" in qa
    assert len(qa["answer"]) > 20
    assert "disclaimer" in qa
    print(f"Q&A answer: {qa['answer'][:150]}")

    es_explanation = await explainer.explain(
        doc, classification, "es")
    assert es_explanation.get("language") == "es"
    assert "disclaimer" in es_explanation
    print(f"ES summary: {es_explanation.get('summary','')[:100]}")

    print("\nALL PHASE 4 ASSERTIONS PASSED")

asyncio.run(run())
