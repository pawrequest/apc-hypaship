from base64 import b64decode

import httpx

from apc_hypaship.config import APCSettings, apc_settings
from apc_hypaship.shipment import Shipment


def book_shipment(
    shipment: dict | Shipment, settings=apc_settings()
) -> httpx.Response:
    """Takes provider ShipmnentDict, or ShipmentAgnost object"""
    shipment_dict = shipment.model_dump(by_alias=True, mode="json")
    res = httpx.post(
        settings.orders_endpoint, headers=settings.headers, json=shipment_dict
    )
    res.raise_for_status()
    return res


def get_label_content(
    shipment_num: str, settings: APCSettings = apc_settings()
) -> bytes:
    params = {"labelformat": "PDF"}
    label = httpx.get(
        settings.one_order_endpoint(shipment_num),
        headers=settings.headers,
        params=params,
    )
    label.raise_for_status()
    content = label.json()["Orders"]["Order"]["Label"]["Content"]
    return b64decode(content)

