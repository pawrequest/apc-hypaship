import httpx
import pytest

from apc_hypaship.client.apc_client import book_shipment
from apc_hypaship.config import apc_date, apc_settings
from apc_hypaship.services import ServiceSpec
from conftest import TEST_DATE

TEST_DATE_STR = apc_date(TEST_DATE)


@pytest.fixture(scope='session')
def booking_response(sample_shipment):
    return book_shipment(shipment=sample_shipment)


def test_service_available(sample_shipment):
    shipment_dict = sample_shipment.model_dump(by_alias=True)

    settings = apc_settings()
    res = httpx.post(settings.services_endpoint, headers=settings.headers, json=shipment_dict, timeout=30)
    res.raise_for_status()
    res_json = res.json()
    avail = res_json['ServiceAvailability']['Services']['Service']
    services = [ServiceSpec(**_) for _ in avail]
    nd = [_ for _ in services if _.ProductCode == 'APCND16']
    assert nd


def test_shipment_export_dict(sample_shipment, sample_shipment_dict):
    assert sample_shipment_dict['Orders']['Order']['CollectionDate'] == apc_date(TEST_DATE)
    assert len(sample_shipment_dict['Orders']['Order']['ShipmentDetails']['Items']['Item']) == sample_shipment.boxes


def test_make_shipment_request(booking_response):
    order_num = booking_response.shipment_num
    assert order_num


def test_download_label(booking_response, tmp_path):
    label_file = tmp_path / 'label.pdf'  # Create a file path inside the temp directory
    label_file.write_bytes(booking_response.label_data)
    assert label_file.exists()
    assert label_file.stat().st_size > 1000

