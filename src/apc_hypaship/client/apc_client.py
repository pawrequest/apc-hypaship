from base64 import b64decode
from typing import Literal

import httpx
from pydantic import BaseModel

from apc_hypaship.config import APCSettings, APC_SETTINGS, apc_settings
from apc_hypaship.reqresp.order_response import (
    BookingResponse,
    Label,
    ResponseType,
    Tracks,
)
from apc_hypaship.shipment import Shipment

ResponseMode = Literal["raw"] | Literal["json"] | type


def export(
    res: httpx.Response,
    mode: ResponseMode = "raw",
) -> ResponseType:
    if mode == "raw":
        return res
    elif mode == "json":
        return res.json()
    elif isinstance(mode, type) and issubclass(mode, BaseModel):
        return mode(**res.json())
    else:
        raise ValueError(f"Invalid mode: {mode}")


def make_post(
    url: str,
    data: dict | None = None,
    mode: ResponseMode = "raw",
    settings: APCSettings = apc_settings(),
) -> ResponseType:
    headers = settings.headers
    res = httpx.post(url, headers=headers, json=data, timeout=30)
    res.raise_for_status()
    return export(res, mode)


def make_get(
    url: str,
    params: dict | None = None,
    mode: ResponseMode = "raw",
    settings: APCSettings = apc_settings(),
) -> ResponseType:
    headers = settings.headers
    res = httpx.get(url, headers=headers, params=params, timeout=30)
    res.raise_for_status()
    return export(res, mode)


def service_available(
    shipment: Shipment,
    mode: ResponseMode = "raw",
    settings: APCSettings = APC_SETTINGS,
) -> ResponseType:
    shipment_dict = shipment.model_dump(by_alias=True, mode="json")
    return make_post(settings.services_endpoint, shipment_dict, mode)


def book_shipment(
    shipment: Shipment,
    settings=apc_settings(),
    mode: ResponseMode = "raw",
) -> ResponseType:
    if isinstance(mode, type) and mode != BookingResponse:
        raise ValueError("When mode is a type, it must be BookingResponse")
    shipment_dict = shipment.model_dump(by_alias=True, mode="json")
    return make_post(
        url=settings.orders_endpoint, data=shipment_dict, mode=mode, settings=settings
    )


def get_label(
    shipment_num: str,
    settings: APCSettings = apc_settings(),
    mode: ResponseMode = "raw",
) -> Label:
    params = {"labelformat": "PDF"}
    label = make_get(
        url=settings.one_order_endpoint(shipment_num),
        params=params,
        mode=BookingResponse,
        settings=settings,
    )
    return export(label.orders.order.label, mode=mode)


def get_tracks(
    shipment_num: str,
    settings: APCSettings = apc_settings(),
) -> Tracks:
    res = make_get(
        url=settings.track_endpoint(shipment_num), mode='json', settings=settings
    )
    t = res.get('Tracks')
    return Tracks(**t)


