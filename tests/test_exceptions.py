"""Tests that proper exceptions are raised."""

import pytest
from requests.exceptions import HTTPError
from ura.constants import CARPARK_AVAILABILITY_ENDPOINT
from ura.exceptions import ApiError
from .test_client import client


class TestAPIErrors:
    def test_http_errors(self, client, requests_mock):
        # configure mock
        requests_mock.get(CARPARK_AVAILABILITY_ENDPOINT, status_code=404)

        with pytest.raises(HTTPError):
            client.carpark_availability()

    def test_api_response_errors(self, client, requests_mock):
        # configure mock
        requests_mock.get(
            CARPARK_AVAILABILITY_ENDPOINT,
            json={"Status": "Error", "Message": "Invalid Input"},
        )

        with pytest.raises(ApiError):
            client.carpark_availability()


class TestParameterError:
    @pytest.mark.parametrize("batch", [5, "5"])
    def test_private_resi_transactions(self, client, batch):
        with pytest.raises(ValueError):
            client.private_resi_transaction(batch)

    @pytest.mark.parametrize("ref_period", [1412, "abcd", "14Q1a"])
    def test_private_resi_rental_contract(self, client, ref_period):
        with pytest.raises(ValueError):
            client.private_resi_rental_contract(ref_period)

    @pytest.mark.parametrize("ref_period", [1234, "1344b"])
    def test_private_resi_developer_sales(self, client, ref_period):
        with pytest.raises(ValueError):
            client.private_resi_developer_sales(ref_period)

    @pytest.mark.parametrize(
        "year,last_dnload_date",
        [
            (2015, "12/05/2012"),
            ("1999", None),
            (1999, None),
            (None, 1234),
            (None, "31/12/2019"),
        ],
    )
    def test_planning_decisions(self, client, year, last_dnload_date):
        with pytest.raises(ValueError):
            client.planning_decisions(year, last_dnload_date)
