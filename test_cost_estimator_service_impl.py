import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from app.services.impl.cost_estimation_service_impl import CostEstimationServiceImpl
from app.schemas.cost_estimator_request import CostEstimatorRequest


@pytest.mark.asyncio
@patch("app.services.impl.cost_estimation_service_impl.BenefitServiceImpl.get_benefit", new_callable=AsyncMock)
@patch("app.services.impl.cost_estimation_service_impl.AccumulatorServiceImpl.get_accumulator", new_callable=AsyncMock)
@patch("app.services.impl.cost_estimation_service_impl.CostEstimatorRepositoryImpl.get_rate", new_callable=AsyncMock)
async def test_estimate_cost_success(mock_get_rate, mock_get_accumulator, mock_get_benefit):
    mock_get_benefit.return_value = {"dummy": "benefit"}
    mock_get_accumulator.return_value = {"dummy": "accumulator"}
    mock_get_rate.return_value = "500"

    payload = {
        "membershipId": "123",
        "zipCode": "85305",
        "benefitProductType": "Medical",
        "languageCode": "EN",
        "service": {
            "code": "99214",
            "type": "CPT4",
            "description": "Office visit",
            "supportingService": {"code": "470", "type": "DRG"},
            "modifier": {"modifierCode": "E1"},
            "diagnosisCode": "F33",
            "placeOfService": {"code": "11"}
        },
        "providerInfo": [{
            "serviceLocation": "000761071",
            "providerType": "HO",
            "speciality": {"code": "91017"},
            "taxIdentificationNumber": "0000431173518",
            "taxIdQualifier": "SN",
            "providerNetworks": {"networkID": "58921"},
            "providerIdentificationNumber": "0004000317",
            "nationalProviderId": "1386660504",
            "providerNetworkParticipation": {"providerTier": "1"}
        }]
    }

    request = CostEstimatorRequest(**payload)
    service = CostEstimationServiceImpl()
    response = await service.estimate_cost(request)
    
    assert response["status"] == "success"
    assert response["rate"] == 500.0
