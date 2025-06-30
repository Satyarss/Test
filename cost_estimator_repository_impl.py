from app.repository.cost_estimator_repository import CostEstimatorRepositoryInterface
from app.database.spanner_client import SpannerClient
from app.config.database_config import spanner_config
from app.config.queries import RATE_QUERIES
from app.core.logger import logger
from app.models.rate_criteria import CostEstimatorRateCriteria

class CostEstimatorRepositoryImpl(CostEstimatorRepositoryInterface):
    def __init__(self):
        """Initialize repository with Spanner client."""
        if not spanner_config.is_valid():
            raise ValueError("Invalid Spanner configuration. Please check environment variables.")
        
        self.db = SpannerClient(
            project_id=spanner_config.project_id,
            instance_id=spanner_config.instance_id,
            database_id=spanner_config.database_id
        )
   
  #  async def get_rate(self, is_out_of_network: bool, rate_criteria: CostEstimatorRateCriteria, *args, **kwargs) -> float:
        """
        Retrieve the rate based on network status and criteria.
        
        Args:
            is_out_of_network: Whether to get out-of-network rate
            rate_criteria: Criteria for rate lookup
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            float: The calculated rate
        """
        # Try claim-based rate first
        """
        params = {
            "service_cd": rate_criteria.service_cd,
            "provider_business_group_nbr": rate_criteria.provider_business_group_nbr,
            "place_of_service_cd": rate_criteria.place_of_service_cd,
            "product_cd": rate_criteria.product_cd,
        }
         

        # Try claim-based rate first
        claim_result = await self._get_claim_based_rate(params)
        if claim_result and len(claim_result) > 0 and claim_result[0].get("RATE") is not None:
            return float(claim_result[0]["RATE"])

        # If not found, try non-standard rate
        non_standard_result = await self._get_non_standard_rate(params)
        if non_standard_result and len(non_standard_result) > 0 and non_standard_result[0].get("RATE") is not None:
            return float(non_standard_result[0]["RATE"])

        # If still not found, try standard rate
        standard_result = await self._get_standard_rate(params)
        if standard_result and len(standard_result) > 0 and standard_result[0].get("RATE") is not None:
            return float(standard_result[0]["RATE"])

        async def _get_claim_based_rate(self, params):
            claim_query = RATE_QUERIES.get("get_claim_based_rate")
            return await self.db.execute_query(claim_query, params)

        async def _get_non_standard_rate(self, params):
            non_standard_query = RATE_QUERIES.get("get_non_standard_rate")
            return await self.db.execute_query(non_standard_query, params)

        async def _get_standard_rate(self, params):
            standard_query = RATE_QUERIES.get("get_standard_rate")
            return await self.db.execute_query(standard_query, params)

       
        return 100.0  # Default rate if no match found
    
        """
    
    async def get_rate(self, is_out_of_network: bool, rate_criteria: CostEstimatorRateCriteria, *args, **kwargs) -> float:
    # STEP 1: Pull provider data directly (no separate method)
        provider_query = RATE_QUERIES.get("get_provider_info")
        provider_params = {
            "provider_identification_nbr": rate_criteria.provider_identification_nbr,
            "network_id": rate_criteria.networkId,
            "service_location_nbr": rate_criteria.serviceLocationNumber
        }
        provider_info = await self.db.execute_query(provider_query, provider_params)
        if provider_info and len(provider_info) > 0:
            rate_criteria.provider_business_group_nbr = provider_info[0].get("PROVIDER_BUSINESS_GROUP_NBR")
            rate_criteria.product_cd = provider_info[0].get("PRODUCT_CD")
            rate_criteria.rating_system_cd = provider_info[0].get("RATING_SYSTEM_CD")
            rate_criteria.geographic_area_cd = provider_info[0].get("GEOGRAPHIC_AREA_CD")

        # STEP 2: Claim-based rate
        claim_query = RATE_QUERIES.get("get_claim_based_rate")
        claim_result = await self.db.execute_query(claim_query, vars(rate_criteria))
        if claim_result and claim_result[0].get("RATE") is not None:
            return float(claim_result[0]["RATE"])

        # STEP 3: Non-standard rate
        if rate_criteria.provider_business_group_nbr:
            non_standard_query = RATE_QUERIES.get("get_non_standard_rate")
            non_standard_result = await self.db.execute_query(non_standard_query, vars(rate_criteria))
            if non_standard_result and non_standard_result[0].get("RATE") is not None:
                return float(non_standard_result[0]["RATE"])

        # STEP 4: Standard rate
        if rate_criteria.provider_business_group_nbr:
            standard_query = RATE_QUERIES.get("get_standard_rate")
        else:
            standard_query = RATE_QUERIES.get("get_standard_rate_without_pbg")

        standard_result = await self.db.execute_query(standard_query, vars(rate_criteria))
        if standard_result and standard_result[0].get("RATE") is not None:
            return float(standard_result[0]["RATE"])

        # STEP 5: Default contract rate (embedded, not as a separate function)
        default_query = RATE_QUERIES.get("get_default_contract_rate")
        default_result = await self.db.execute_query(default_query, vars(rate_criteria))
        if default_result and default_result[0].get("RATE") is not None:
            return float(default_result[0]["RATE"])

        # Final fallback
        return 0.0




   