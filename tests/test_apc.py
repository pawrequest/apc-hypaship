import pytest

from apc_hypaship.apc_client import (
    book_shipment,
    get_label,
    get_tracks,
    service_available,
)
from apc_hypaship.config import apc_date
from conftest import TEST_DATE

TEST_DATE_STR = apc_date(TEST_DATE)



def test_service_available(sample_shipment, sample_settings):
    res = service_available(shipment=sample_shipment, settings=sample_settings)
    avail = res.service_availability.services.service
    nd = [_ for _ in avail if _.product_code == "APCND16"]
    assert nd


def test_book_shipment(sample_booking_response):
    assert sample_booking_response.orders.messages.code == "SUCCESS"
    assert sample_booking_response.orders.order.order_number


def test_get_label(sample_booking_response, sample_settings):
    label = get_label(sample_booking_response.order_num, settings=sample_settings)
    label_content = label.content
    assert label_content


def test_get_tracks(sample_booking_response, sample_settings):
    res = get_tracks(sample_booking_response.order_num, settings=sample_settings)
    assert res.messages.code == "SUCCESS"
