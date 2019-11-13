"""Endpoint constants and configurations for requests"""

BASE_API_DOMAIN = "https://www.ura.gov.sg"
BASE_API_ENDPOINT = "{}/uraDataService".format(BASE_API_DOMAIN)
BASE_SERVICE_ENDPOINT = "{}/invokeUraDS?service=".format(BASE_API_ENDPOINT)

AUTHENTICATION_ENDPOINT = "{}/insertNewToken.action".format(BASE_API_ENDPOINT)

# Carpark related endpoints
CARPARK_AVAILABILITY_ENDPOINT = "{}Car_Park_Availability".format(BASE_SERVICE_ENDPOINT)
CARPARK_DETAILS_ENDPOINT = "{}Car_Park_Details".format(BASE_SERVICE_ENDPOINT)
SEASON_CARPARK_DETAILS_ENDPOINT = "{}Season_Car_Park_Details".format(
    BASE_SERVICE_ENDPOINT
)

# Private Residential Property
PRIVATE_RESI_TRANSACTION_ENDPOINT = "{}PMI_Resi_Transaction".format(
    BASE_SERVICE_ENDPOINT
)
PRIVATE_NONLANDED_RESI_RENTAL_MEDIAN_ENDPOINT = "{}PMI_Resi_Rental_Median".format(
    BASE_SERVICE_ENDPOINT
)
PRIVATE_RESI_RENTAL_CONTRACT_ENDPOINT = "{}PMI_Resi_Rental".format(
    BASE_SERVICE_ENDPOINT
)
PRIVATE_RESI_DEVELOPER_SALES_ENDPOINT = "{}PMI_Resi_Developer_Sales".format(
    BASE_SERVICE_ENDPOINT
)
PRIVATE_RESI_PIPELINE_ENDPOINT = "{}PMI_Resi_Pipeline".format(BASE_SERVICE_ENDPOINT)

# Planning Decisions
PLANNING_DECISIONS_ENDPOINT = "{}Planning_Decision".format(BASE_SERVICE_ENDPOINT)

# Approved Use related endpoints
APPROVED_RESI_USE_ENDPOINT = "{}EAU_Appr_Resi_Use".format(BASE_SERVICE_ENDPOINT)

# Request session settings
MAX_RETRIES = 3
TIMEOUT = 10
