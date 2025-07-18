import copy
from fastapi.testclient import TestClient
from app.main import app
from app.core.exception_responses import responses

client = TestClient(app)

valid_payload = {
    "membershipId": "5~186103331+10+7+20240101+793854+BA+829",
    "zipCode": "85305",
    "benefitProductType": "Medical",
    "languageCode": "11",
    "service": {
        "code": "99214",
        "type": "CPT4",
        "description": "Adult Office visit Age 30-39",
        "supportingService": {
            "code": "470",
            "type": "DRG"
        },
        "modifier": {
            "modifierCode": "E1"
        },
        "diagnosisCode": "F33 40",
        "placeOfService": {
            "code": "11"
        }
    },
    "providerInfo": [
        {
            "serviceLocation": "000761071",
            "providerType": "HO",
            "specialty": {
                "code": "91017"
            },
            "taxIdentificationNumber": "0000431173518",
            "taxIdQualifier": "SN",
            "providerNetworks": {
                "networkID": "58921"
            },
            "providerIdentificationNumber": "0004000317",
            "nationalProviderId": "1386660504",
            "providerNetworkParticipation": {
                "providerTier": "1"
            }
        }
    ]
}


def test_response_200_structure():
    response_200 = responses.get(200)
    assert response_200 is not None
    assert "description" in response_200
    assert "headers" in response_200
    assert "x-clientrefid" in response_200["headers"]
    assert "x-correlation-id" in response_200["headers"]


def test_response_400_structure():
    response_400 = responses.get(400)
    assert response_400 is not None
    assert response_400["status"] == 400
    assert response_400["title"] == "One or more validation errors occurred"
    assert response_400["type"] == "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1"
    assert "correlationId" in response_400
    assert "detail" in response_400
    assert "errors" in response_400
    assert "message" in response_400




def test_400_response_matches_exception_responses_model():
    # Remove required field to trigger validation error
    payload = copy.deepcopy(valid_payload)
    del payload["membershipId"]

    response = client.post("/costestimator/v1/rate", json=payload)

    assert response.status_code == 400

    actual = response.json()
    expected = responses[400]

    assert actual["status"] == expected["status"]
    assert actual["title"] == expected["title"]
    assert actual["type"] == expected["type"]
    assert actual["detail"] == expected["detail"]
    assert "errors" in actual
    assert "message" in actual
    assert "correlationId" in actual
