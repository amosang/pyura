"""Test that the Client is working properly."""

import pytest
import os

from ura import Client
from datetime import date, timedelta


@pytest.fixture(scope="module")
def client():
    key = os.environ["URA_ACCESS_KEY"]
    client = Client(key)
    client.get_token()

    return client


class TestCarpark:
    def test_carpark_availability(self, client):
        result = client.carpark_availability()

        assert isinstance(result, list)
        assert len(result) > 0

    def test_carpark_details(self, client):
        result = client.carpark_details()

        assert isinstance(result, list)
        assert len(result) > 0

    def test_season_carpark_details(self, client):
        result = client.season_carpark_details()

        assert isinstance(result, list)
        assert len(result) > 0


class TestPrivateResidentialProperty:
    @pytest.mark.parametrize("batch", [1])
    def test_private_resi_transactions(self, client, batch):
        result = client.private_resi_transaction(batch)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_private_nl_resi_rental_median(self, client):
        result = client.private_nl_resi_rental_median()

        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.parametrize("ref_period", ["19q1"])
    def test_private_resi_rental_contract(self, client, ref_period):
        result = client.private_resi_rental_contract(ref_period)

        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.parametrize("ref_period", ["0919"])
    def test_private_resi_developer_sales(self, client, ref_period):
        result = client.private_resi_developer_sales(ref_period)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_private_resi_pipeline(self, client):
        result = client.private_resi_pipeline()

        assert isinstance(result, list)
        assert len(result) > 0


class TestPlanningDecisions:
    @pytest.mark.parametrize(
        "year,last_dnload_date",
        [
            (2015, None),
            (None, (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")),
        ],
    )
    def test_planning_decisions(self, client, year, last_dnload_date):
        result = client.planning_decisions(year, last_dnload_date)

        assert isinstance(result, list)
        assert len(result) > 0


class TestApprovedUse:
    @pytest.mark.parametrize(
        "blk_house_no,street,storey_no,unit_no",
        [(196, "Rivervale Drive", 11, 725), (196, "Rivervale Drive", None, None)],
    )
    def test_approved_resi_use(self, client, blk_house_no, street, storey_no, unit_no):
        approved_resi_use = client.approved_resi_use(
            blk_house_no, street, storey_no, unit_no
        )

        assert isinstance(approved_resi_use, str)
