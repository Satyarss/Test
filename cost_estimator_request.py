from typing import Annotated
from typing import List

from pydantic import BaseModel, Field, root_validator
from typing import Optional


class SupportingService(BaseModel):
    code: str
    type: str


class Modifier(BaseModel):
    modifierCode: str


class PlaceOfService(BaseModel):
    code: str


class Specialty(BaseModel):
    code: Annotated[
        str, Field(..., json_schema_extra={"examples": ["91017"]}, min_length=1)
    ]


class ProviderNetworks(BaseModel):
    networkID: str


class NationalProviderIdentifier(BaseModel):
    nationalProviderId: str



class ProviderNetworkParticipation(BaseModel):
    providerTier: str


class ProviderInfo(BaseModel):
    serviceLocation: str
    providerType: str
    specialty: Optional[Specialty] = None
    speciality: Optional[Specialty] = None
    taxIdentificationNumber: str
    taxIdQualifier: str
    providerNetworks: ProviderNetworks
    providerIdentificationNumber: str
    nationalProviderId: Optional[str] = None
    nationalProviderIdentifier: Optional[NationalProviderIdentifier] = None
    providerNetworkParticipation: ProviderNetworkParticipation
    
    @root_validator(pre=True)
    def normalize_fields(cls, values):

        if 'specialty' not in values and 'speciality' in values:
            values['specialty'] = values['speciality']

        if 'nationalProviderId' not in values and 'nationalProviderIdentifier' in values:
            npi = values.get('nationalProviderIdentifier')
            if isinstance(npi, dict) and 'nationalProviderId' in npi:
                values['nationalProviderId'] = npi['nationalProviderId']

        return values



class Service(BaseModel):
    code: str
    type: str
    description: str
    supportingService: SupportingService
    modifier: Modifier
    diagnosisCode: str
    placeOfService: PlaceOfService


class CostEstimatorRequest(BaseModel):
    membershipId: str
    zipCode: str
    benefitProductType: str
    languageCode: str
    service: Service
    providerInfo: List[ProviderInfo]


class ProviderType(BaseModel):
    code: str


class ProviderSpecialty(BaseModel):
    code: str


class ServiceCodeInfo(BaseModel):
    providerType: List[ProviderType]
    placeOfService: List[PlaceOfService]
    providerSpecialty: List[ProviderSpecialty]
    code: str
    type: str


class ServiceInfo(BaseModel):
    serviceCodeInfo: ServiceCodeInfo


class RequestModel(BaseModel):
    benefitProductType: str
    membershipID: str
    planIdentifier: str
    serviceInfo: List[ServiceInfo]
