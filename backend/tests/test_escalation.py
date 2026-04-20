import pytest
from src.core.escalation import EscalationRouter

@pytest.fixture
def router():
    return EscalationRouter()

def test_route_standard_category(router):
    classification = {"document_category": "contract", "jurisdiction_name": "Unknown"}
    result = router.route(classification)

    assert result["disclaimer_level"] == "standard"
    assert result["show_attorney_warning"] is False
    assert result["show_public_defender_info"] is False
    assert result["escalation_color"] == "green"
    assert any("lawhelp.org" in link["url"] for link in result["resource_links"])

def test_route_elevated_category(router):
    classification = {"document_category": "government_form", "jurisdiction_name": "Unknown"}
    result = router.route(classification)

    assert result["disclaimer_level"] == "standard"
    assert result["show_attorney_warning"] is True
    assert result["show_public_defender_info"] is False
    assert result["escalation_color"] == "yellow"

def test_route_criminal_category(router):
    classification = {"document_category": "criminal_charge", "jurisdiction_name": "Unknown"}
    result = router.route(classification)

    assert result["disclaimer_level"] == "criminal"
    assert result["show_attorney_warning"] is True
    assert result["show_public_defender_info"] is True
    assert result["escalation_color"] == "red"
    assert result["pre_analysis_warning"] is not None
    assert "criminal" in result["pre_analysis_warning"].lower()

def test_route_plea_agreement(router):
    classification = {"document_category": "plea_agreement", "jurisdiction_name": "Unknown"}
    result = router.route(classification)

    assert result["disclaimer_level"] == "plea"
    assert result["show_attorney_warning"] is True
    assert result["show_public_defender_info"] is True
    assert result["escalation_color"] == "red"
    assert "plea" in result["pre_analysis_warning"].lower()

def test_route_unknown_category_defaults_to_standard(router):
    classification = {"document_category": "completely_unknown", "jurisdiction_name": "Unknown"}
    result = router.route(classification)

    assert result["disclaimer_level"] == "standard"
    assert result["escalation_color"] == "green"

def test_route_spanish_language(router):
    classification = {"document_category": "contract", "jurisdiction_name": "Unknown"}
    result = router.route(classification, lang="es")

    # Check for Spanish labels in resource links
    assert any("ayuda legal" in link["label"].lower() for link in result["resource_links"])

def test_route_with_jurisdiction_legal_aid(router):
    # California is in jurisdictions.json and has a legal_aid_url
    classification = {"document_category": "contract", "jurisdiction_name": "California"}
    result = router.route(classification)

    # Should have the 3 default links + 1 jurisdiction specific link
    assert len(result["resource_links"]) == 4
    assert any("lawhelpca.org" in link["url"] for link in result["resource_links"])
    assert any("Legal aid in your state" == link["label"] for link in result["resource_links"])

def test_route_with_jurisdiction_legal_aid_spanish(router):
    classification = {"document_category": "contract", "jurisdiction_name": "California"}
    result = router.route(classification, lang="es")

    assert any("Ayuda legal en su estado" == link["label"] for link in result["resource_links"])

def test_route_missing_keys_in_classification(router):
    # Should not crash and use defaults
    result = router.route({})

    assert result["disclaimer_level"] == "standard"
    assert result["escalation_color"] == "green"
    assert len(result["resource_links"]) == 3
