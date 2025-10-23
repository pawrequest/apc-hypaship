# import sys
# from datetime import date, timedelta
# from pathlib import Path
#
# import pytest
#
# from apc_hypaship.config import APCSettings
# from apc_hypaship.apc_client import APCClient
# from apc_hypaship.models.response.resp import BookingResponse
# from apc_hypaship.models.request.address import Address, Contact
# from apc_hypaship.models.request.services import APCServiceCode
# from apc_hypaship.models.request.shipment import GoodsInfo, Order, Shipment, ShipmentDetails
#
# TEST_DATE = date.today() + timedelta(days=2)
# if TEST_DATE.weekday() in (5, 6):
#     TEST_DATE += timedelta(days=7 - TEST_DATE.weekday())
#
#
# @pytest.fixture
# def LIVE_SETTINGS():
#     LIVE_ENV = Path(r'C:\prdev\envs\amdev\live\apc.env')
#     return APCSettings.from_env_file(LIVE_ENV)
#
#
# @pytest.fixture
# def LIVE_CLIENT(LIVE_SETTINGS):
#     return APCClient(settings=LIVE_SETTINGS)
#
#
# def test_service_available(sample_shipment, sample_client):
#     res = sample_client.fetch_service_available(shipment=sample_shipment)
#     avail = res.service_availability.services.service
#     print('\n\nAvailable Services:')
#     for svc in avail:
#         print(svc)
#     nd = [_ for _ in avail if _.product_code == 'APCND16']
#     assert nd
#
