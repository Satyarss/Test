SELECT PAYMENT_METHOD_CD, RATE
FROM CET_RATES
WHERE
    SERVICE_CD = @servicecd
    AND SERVICE_TYPE_CD = @servicetype
    AND PLACE_OF_SERVICE_CD = @placeofservice
    AND PRODUCT_CD = @productcd
    AND PROVIDER_BUSINESS_GROUP_NBR IN UNNEST(@providerbusinessgroupnbr)
    AND CONTRACT_TYPE IN ('D', 'C', 'N')
