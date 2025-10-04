import sys
from datetime import date, timedelta

import pytest

from apc_hypaship.config import APCSettings
from apc_hypaship.apc_client import APCClient
from apc_hypaship.models.response.resp import BookingResponse
from apc_hypaship.models.request.address import Address, Contact
from apc_hypaship.models.request.services import APC_SERVICES_DICT
from apc_hypaship.models.request.shipment import GoodsInfo, Order, Shipment, ShipmentDetails

TEST_DATE = date.today() + timedelta(days=2)
if TEST_DATE.weekday() in (5, 6):
    TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())


@pytest.fixture
def sample_settings():
    return APCSettings.from_env('APC_ENV')


@pytest.fixture(autouse=True)
def sandbox_only(sample_settings):
    if 'training' not in sample_settings.base_url:
        pytest.skip('Skipping tests outside sandbox environment')
        sys.exit()


@pytest.fixture
def sample_client(sample_settings):
    return APCClient(settings=sample_settings)


@pytest.fixture
def sample_contact():
    yield Contact(
        person_name='Test Contact name',
        mobile_number='07666666666',
        email='dsvkndslvn@dzv.com',
    )


@pytest.fixture
def sample_address(sample_contact):
    yield Address(
        postal_code='DA16 3HU',
        address_line_1='25 Bennet Close',
        city='Welling',
        country_code='GB',
        contact=sample_contact,
        company_name='Test Company',
    )


@pytest.fixture
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
def sample_bad_order(sample_order) -> Order:
    order = sample_order.model_copy(deep=True)
    order.delivery = None
    return order


@pytest.fixture
def sample_shipment(sample_order) -> Shipment:
    return Shipment.from_order(sample_order)


@pytest.fixture
def sample_bad_shipment(sample_bad_order) -> Shipment:
    shipment = Shipment.from_order(sample_bad_order)
    return shipment


@pytest.fixture
def sample_booking_response(sample_shipment, sample_client) -> BookingResponse:
    return sample_client.fetch_book_shipment(sample_shipment)



