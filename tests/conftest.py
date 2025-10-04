import os
import sys

from apc_hypaship.config import APCSettings


from apc_hypaship.apc_client import book_shipment


from apc_hypaship.models.response.resp import BookingResponse


from datetime import date, timedelta

import pytest

from apc_hypaship.models.request.address import Address, Contact
from apc_hypaship.models.request.services import APC_SERVICES_DICT
from apc_hypaship.models.request.shipment import GoodsInfo, Order, Shipment, ShipmentDetails


TEST_DATE = date.today() + timedelta(days=2)
if TEST_DATE.weekday() in (5, 6):
    TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())


@pytest.fixture(scope='session')
def sample_settings():
    return APCSettings.from_env('APC_ENV')


@pytest.fixture(autouse=True)
def sandbox_only(sample_settings):
    if 'training' not in sample_settings.base_url:
        pytest.skip('Skipping tests outside sandbox environment')
        sys.exit()


@pytest.fixture(scope='session')
def sample_contact():
    yield Contact(
        person_name='Test Contact name',
        mobile_number='07666666666',
        email='dsvkndslvn@dzv.com',
    )


@pytest.fixture(scope='session')
def sample_address(sample_contact):
    yield Address(
        postal_code='DA16 3HU',
        address_line_1='25 Bennet Close',
        city='Welling',
        country_code='GB',
        contact=sample_contact,
        company_name='Test Company',
    )


@pytest.fixture(scope='session')
def sample_order(sample_address) -> Order:
    return Order(
        collection_date=TEST_DATE,
        product_code=APC_SERVICES_DICT['NEXT_DAY'],
        reference='Test Reference',
        delivery=sample_address,
        goods_info=GoodsInfo(),
        shipment_details=ShipmentDetails(number_of_pieces=1),
    )


@pytest.fixture
def sample_shipment(sample_order) -> Shipment:
    return Shipment.from_order(sample_order)


@pytest.fixture
def sample_shipment_dict(sample_shipment) -> dict:
    return sample_shipment.model_dump(by_alias=True, mode='json')


@pytest.fixture
def sample_booking_response(sample_shipment, sample_settings) -> BookingResponse:
    return book_shipment(sample_shipment, sample_settings)

