import os

os.environ["APC_ENV"] = r"C:\prdev\envs\sandbox\apc.env"
from datetime import date, timedelta

import pytest

from apc_hypaship.address import Address, Contact
from apc_hypaship.config import apc_settings
from apc_hypaship.services import APC_SERVICES_DICT
from apc_hypaship.shipment import GoodsInfo, Order, Shipment, ShipmentDetails


TEST_DATE = date.today() + timedelta(days=2)
if TEST_DATE.weekday() in (5, 6):
    TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())


@pytest.fixture(scope="session")
def settings():
    return apc_settings()


@pytest.fixture(scope="session")
def sample_contact():
    yield Contact(
        person_name="Test Contact name",
        mobile_number="07666666666",
        email="dsvkndslvn@dzv.com",
    )


@pytest.fixture(scope="session")
def sample_address(sample_contact):
    yield Address(
        postal_code="DA16 3HU",
        address_line_1="25 Bennet Close",
        city="Welling",
        country_code="GB",
        contact=sample_contact,
    )


@pytest.fixture(scope="session")
def sample_order(sample_address) -> Order:
    return Order(
        collection_date=TEST_DATE,
        product_code=APC_SERVICES_DICT["NEXT_DAY"],
        reference="Test Reference",
        delivery=sample_address,
        goods_info=GoodsInfo(),
        shipment_details=ShipmentDetails(number_of_pieces=1),
    )


@pytest.fixture
def sample_shipment(sample_order) -> Shipment:
    return Shipment.from_order(sample_order)

