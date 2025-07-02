Need to write the code that will retrieve rates from spanner

 

Assumptions: 

Rates tables are available in spanner

We have a request to the cost estimation API

Steps Required:

Validate request

Parse cost estimator request, prepare query to find standard contract rate

Returns the rates for standard contract.

 

Deliverable:

Logic to return rate

Unit test the logic

Here logic we need to implement, when we pull rate from spanner 


Extract below parameter from CostAPI Request. Other optional parameter, we do after completion of below story. 

Provider Identification Number  - 

Service Location Number - 

Network Id - 

Service Code 

Service Type

Place of service code

While execute query we need to implement below logic.

Check Claim table first




SELECT
  MAX(c.rate) AS max_rate
FROM
  CET_CLAIM_BASED_AMOUNTS c
WHERE
  c.PROVIDER_IDENTIFICATION_NBR = '0009864111'
  AND c.NETWORK_ID = '11624'
  AND c.PLACE_OF_SERVICE_CD = '11'
  AND c.SERVICE_CD = '73000'
  AND c.SERVICE_TYPE_CD = 'CPT'
If there is no record in claim get PROVIDER_BUSINESS_GROUP_NBR, Product code, Rating System code, GEOGRAPHIC_AREA_CD, Network_id from provider table. 



select PRODUCT_CD,RATING_SYSTEM_CD,PROVIDER_BUSINESS_GROUP_NBR,EPDB_GEOGRAPHIC_AREA_CD from CET_PROVIDERS where PROVIDER_IDENTIFICATION_NBR = '4399827'
AND NETWORK_ID = '12941'
AND SERVICE_LOCATION_NBR = '8071678'
if PROVIDER_BUSINESS_GROUP_NBR is null then, execute below query. 

select MAX(rate) from CET_RATES where SERVICE_CD = 'G9551' and SERVICE_TYPE_CD = 'HCPC' and RATE_SYSTEM_CD = 'REF' and PRODUCT_CD = 'MEPO' and GEOGRAPHIC_AREA_CD = 'FL04' and PLACE_OF_SERVICE_CD = '22' and CONTRACT_TYPE = 'S'
