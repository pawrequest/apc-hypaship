import pytest

from apc_hypaship.config import apc_date
from apc_hypaship.models.request.shipment import Shipment
from apc_hypaship.models.response.common import APCException
from conftest import TEST_DATE, sample_client

TEST_DATE_STR = apc_date(TEST_DATE)


def test_service_available(sample_shipment, sample_client):
    res = sample_client.fetch_service_available(shipment=sample_shipment)
    avail = res.service_availability.services.service
    nd = [_ for _ in avail if _.product_code == 'APCND16']
    assert nd


def test_book_shipment(sample_booking_response):
    assert sample_booking_response.orders.messages.code == 'SUCCESS'
    assert sample_booking_response.orders.order.order_number


def test_get_label(sample_booking_response, sample_client):
    label = sample_client.fetch_label(sample_booking_response.order_num)
    label_content = label.content
    assert label_content


def test_get_tracks(sample_booking_response, sample_client):
    res = sample_client.fetch_tracks(sample_booking_response.order_num)
    assert res.messages.code == 'SUCCESS'


def test_bad_postcode(sample_order, sample_client):
    order = sample_order.model_copy(deep=True)
    order.delivery.postal_code = 'XXXX XXX'
    shipment = Shipment.from_order(order)

    with pytest.raises(APCException) as excinfo:
        res = sample_client.fetch_book_shipment(shipment)
    assert 'Delivery PostalCode' in str(excinfo.value.args[0])
    assert excinfo.value.code == '201'
