import pytest

from apc_hypaship.client.apc_client import (
    book_shipment,
    get_label,
    get_tracks,
    service_available,
)
from apc_hypaship.config import apc_date
from apc_hypaship.services import ServiceSpec
from conftest import TEST_DATE

TEST_DATE_STR = apc_date(TEST_DATE)


@pytest.fixture(scope="session")
def booking_response(sample_shipment):
    return book_shipment(shipment=sample_shipment)


def test_service_available(sample_shipment, settings):
    res = service_available(shipment=sample_shipment, settings=settings)
    res_json = res.json()
    avail = res_json["ServiceAvailability"]["Services"]["Service"]
    services = [ServiceSpec(**_) for _ in avail]
    nd = [_ for _ in services if _.ProductCode == "APCND16"]
    assert nd


def test_book_shipment(sample_booking_response, settings):
    assert sample_booking_response.orders.messages.code == "SUCCESS"
    assert sample_booking_response.orders.order.order_number


def test_get_label_bytest(sample_booking_response):
    label = get_label(sample_booking_response.order_num)
    label_content = label.content
    assert label_content


def test_get_tracks(sample_booking_response, settings):
    res = get_tracks(sample_booking_response.order_num)
    ...
