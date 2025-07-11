from typing import List, Dict, Any
from app.schemas.cost_estimator_request import CostEstimatorRequest
from app.schemas.benefit_request import BenefitRequest
from app.models.rate_criteria import CostEstimatorRateCriteria


class CostEstimatorMapper:
    @staticmethod
    def to_benefit_request(request: CostEstimatorRequest) -> BenefitRequest:
        """
        Maps a RequestModel to a BenefitRequest.

        Args:
            request (RequestModel): The input request model

        Returns:
            BenefitRequest: The mapped benefit request
        """
        service_info = {
            "serviceCodeInfo": {
                "code": request.service.code,
                "type": request.service.type,
                "providerType": [
                    {"code": provider.providerType} for provider in request.providerInfo
                ],
                "placeOfService": [{"code": request.service.placeOfService.code}],

                "providerSpecialty": [
                    {
                        "code" : (
                            provider.specialty.code 
                            if provider.specialty 
                            else provider.speciality.code

                        )
                    }
                    for provider in request.providerInfo
                ]
            }
        }

        return BenefitRequest(
            benefitProductType=request.benefitProductType,
            membershipID=request.membershipId,
            planIdentifier="3~",  # Using membershipId as planIdentifier
            serviceInfo=[service_info],
        )

    @staticmethod
    def to_rate_criteria(request: CostEstimatorRequest) -> CostEstimatorRateCriteria:
        """
        Maps a RequestModel to CostEstimatorRateCriteria.

        Args:
            request (CostEstimatorRequest): The input request model

        Returns:
            CostEstimatorRateCriteria: The mapped rate criteria
        """
        # Debug: Print the available fields
        print(
            "CostEstimatorRateCriteria fields:",
            CostEstimatorRateCriteria.__annotations__,
        )

        # Determine isOutofNetwork based on providerInfo availability
        # If providerInfo is null/empty, set isOutofNetwork to True, otherwise False
        is_out_of_network = not request.providerInfo or len(request.providerInfo) == 0

        try:
            # Handle case where providerInfo might be empty
            if not request.providerInfo or len(request.providerInfo) == 0:
                # Set default values when providerInfo is not available
                return CostEstimatorRateCriteria(
                    providerIdentificationNumber="",
                    serviceCode=request.service.code,
                    serviceType=request.service.type,
                    # serviceLocationNumber="",
                    # networkId="",
                    placeOfService=request.service.placeOfService.code,
                    zipCode=request.zipCode,
                    isOutofNetwork=True,
                )
            else:
                # Use the first providerInfo when available
                return CostEstimatorRateCriteria(
                    providerIdentificationNumber=(
                        getattr (request.providerInfo[0], "providerIdentificationNumber", None)
                        or getattr(request.providerInfo[0], "nationalProviderId", None)
                        or (
                            request.providerInfo[0].nationalProviderIdentifier.nationalProviderId
                            if request.providerInfo[0].nationalProviderIdentifier
                            else ""
                            
                        )
                    ),
                    serviceCode=request.service.code,
                    serviceType=request.service.type,
                    serviceLocationNumber=request.providerInfo[0].serviceLocation,
                    networkId=request.providerInfo[0].providerNetworks.networkID,
                    placeOfService=request.service.placeOfService.code,
                    zipCode=request.zipCode,
                    isOutofNetwork=False,
                )
        except Exception as e:
            print(f"Error creating CostEstimatorRateCriteria: {e}")
            raise
