import os

from apc_hypaship.apc_client import service_available

os.environ['APC_ENV'] = r'C:\prdev\envs\sandbox\apc.env'



def test_service_available(sample_shipment, test_settings):
    res = service_available(shipment=sample_shipment, settings=test_settings)
    avail = res.service_availability.services.service
    nd = [_ for _ in avail if _.product_code == "APCND16"]
    assert nd
