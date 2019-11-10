from requests import Session
from requests.adapters import HTTPAdapter

from .constants import *
from requests.auth import AuthBase
from .exceptions import ApiError
import re


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme for URA service.

        Attributes:
            key (str): URA access key from email.
            token (str): URA token to be used for the day’s access to the API.
    """

    def __init__(self, key, token):
        self._key = key
        self._token = token

    def __call__(self, r):
        """Attaches an API token to the custom auth header."""
        r.headers["AccessKey"] = self._key
        r.headers["Token"] = self._token
        return r


class Client:
    """Interacts with URA endpoints. https://www.ura.gov.sg/maps/api/ .

        Attributes:
            key (str): URA access key from email. Request for one at https://www.ura.gov.sg/maps/api/reg.html
            token (str): URA token to be used for the day’s access to the API.
            session (Session): Request session which provides cookie persistence, connection-pooling, and configuration.
    """

    def __init__(self, key):

        self._session = Session()
        self._session.mount("https://", HTTPAdapter(max_retries=MAX_RETRIES))

        self._key = key
        self._token = None

    def get_token(self):
        """ Retrieves a token to be used for the day’s access to the API"""
        headers = {"AccessKey": self._key}
        response = self._session.get(AUTHENTICATION_ENDPOINT, headers=headers)
        self._token = response.json()["Result"]
        self._session.auth = TokenAuth(self._key, self._token)

    def _send_request(self, endpoint, **kwargs):
        """Send a request to an endpoint

        Args:
            endpoint (str): The endpoint to send the request to.
            **kwargs: Optional, key-value pairs to be passed as parameters to the endpoint.

        Returns:
            dict or list: response's json content of the request

        Raises:
            HTTPError: Raised if there's a network error of 4xx or 5xx
            ApiError: Raised if there's an unsuccessful response from endpoint
        """
        params = {key: value for key, value in kwargs.items()}

        response = self._session.get(endpoint, params=params, timeout=TIMEOUT)
        response.raise_for_status()

        response_json = response.json()

        # due to inconsistencies with api endpoints
        status = response_json.get("Status", None) or response_json.get("status", None)
        message = response_json.get("Message", None) or response_json.get(
            "message", None
        )

        # checks for Success as ura endpoint returns 200 even if Failure occurs
        if status != "Success":
            raise ApiError(message, response_json)

        # returns data which is usually contained in 'Result'
        if "Result" in response_json:
            response_data = response_json["Result"]
        else:
            response_data = response_json
        return response_data

    def carpark_availability(self):
        """Gets a list of URA car park available lots.

        Returns:
            list: list of URA carpark available lots.
        """

        response_data = self._send_request(CARPARK_AVAILABILITY_ENDPOINT)
        return response_data

    def carpark_details(self):
        """Gets a list of URA car park details.

        Returns:
            list: list of URA car park details.
        """
        response_data = self._send_request(CARPARK_DETAILS_ENDPOINT)
        return response_data

    def season_carpark_details(self):
        """Gets a list of URA season car park details and rates available for application.
        
        Returns:
            list: list of URA season car park details and rates available for application.
        """
        response_data = self._send_request(SEASON_CARPARK_DETAILS_ENDPOINT)
        return response_data

    def private_resi_transaction(self, batch):
        """Gets a batch of the past 3 years of private residential property transaction records.

        Args:
            batch (int): Specify batch to retrieve. Data are available for download in 4 batches.

        Returns:
            list: list of record transactions.

        Raises:
            ValueError: Raised if batch is between 1 and 4.
        """
        # ensure params follow API requirements
        if int(batch) not in range(1, 5):
            raise ValueError("Should be in range 1 : 4")

        response_data = self._send_request(
            PRIVATE_RESI_TRANSACTION_ENDPOINT, batch=batch
        )

        return response_data

    def private_nl_resi_rental_median(self):
        """Gets past 3 years of median rentals of private non-landed residential properties with at least 10 rental
        contracts for the reference period.
        
        Returns:
            list: list of rental median for reference periods
        """
        response_data = self._send_request(
            PRIVATE_NONLANDED_RESI_RENTAL_MEDIAN_ENDPOINT
        )
        return response_data

    def private_resi_rental_contract(self, ref_period):
        """Gets past 3 years of private residential properties with rental contracts submitted to IRAS
        for Stamp Duty assessment.

        Args:
            ref_period (str): Specify reference quarter to retrieve. Field is in format of yyqq.

        Returns:
            list: list of properties with their rental contracts.

        Raises:
            ValueError: Raised if ref_period is not in the format of yyqq.
        """
        # ensure params follow API requirements
        pattern = re.compile(r"^\d{2}[qQ][1-4]$")
        if not pattern.match(str(ref_period)):
            raise ValueError("Should be of format yyqq e.g. 14q1 or 05Q4")

        response_data = self._send_request(
            PRIVATE_RESI_RENTAL_CONTRACT_ENDPOINT, refPeriod=ref_period
        )
        return response_data

    def private_resi_developer_sales(self, ref_period):
        """Gets 3 years of prices of completed and uncompleted private residential units and executive condominiums
        with pre-requisite for sale sold by developers.

        Args:
            ref_period (str): Specify reference quarter to retrieve. Field is in format of mmyy.

        Returns:
            list: list of properties with the developer sales.

        Raises:
            ValueError: Raised if ref_period is not in the format of mmyy.

        """
        # ensure params follow API requirements
        pattern = re.compile(r"^(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$")
        if not pattern.match(str(ref_period)):
            raise ValueError("Should be of format mmyy e.g. 0913")

        response_data = self._send_request(
            PRIVATE_RESI_DEVELOPER_SALES_ENDPOINT, refPeriod=ref_period
        )
        return response_data

    def private_resi_pipeline(self):
        """Gets the latest quarter of project pipeline data.

        Returns:
            list: list of projects.
        """
        response_data = self._send_request(PRIVATE_RESI_PIPELINE_ENDPOINT)
        return response_data

    def planning_decisions(self, year=None, last_dnload_date=None):
        """Gets information on Written Permission granted or rejected by URA.

        Args:
            year (int): Specify year of data to download. Only records after year 2000 can be retrieved.
            last_dnload_date: Specify created, modified or deleted from this date till present.
                              Date is in dd/mm/yyyy format and it cannot be more than one year ago.

        Returns:
            list: list of planning decisions.

        Raises:
            ValueError: Raised if any of the following occurs
            (1) year and last_dnload_date are provided.
            (2) year is before 2000.
            (3) last_dnload_date is not of format dd/mm/yyyy.
        """
        # ensure params follow API requirements
        pattern = re.compile(r"^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$")
        if year and last_dnload_date:
            raise ValueError(
                "Service accepts either one but not both year and last_dnload_date parameter."
            )

        if year:
            if int(year) < 2000:
                raise ValueError("Should be after year 2000")

        if last_dnload_date:
            if not pattern.match(str(last_dnload_date)):
                raise ValueError("Should be of format dd/mm/yyyy")

        response_data = self._send_request(
            PLANNING_DECISIONS_ENDPOINT, year=year, last_dnload_date=last_dnload_date
        )

        return response_data

    def approved_resi_use(self, blk_house_no, street, storey_no=None, unit_no=None):
        """Gets information on whether an address is approved for Residential use.
        
        Args:
            blk_house_no (str): The blk/house number of the address
            street (str): The street of the address
            storey_no (str): Optional, The storey number of the address.
            unit_no (str): Optional, The unit number of the address.

        Returns:
            str: String indicating whether the address is approved for Residential use.
        """
        response_json = self._send_request(
            APPROVED_RESI_USE_ENDPOINT,
            blkHouseNo=blk_house_no,
            street=street,
            storeyNo=storey_no,
            unit_no=unit_no,
        )

        response_data = response_json["isResiUse"]
        return response_data
