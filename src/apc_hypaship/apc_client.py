"""HTTP client for the APC Hypaship v3 JSON API."""

from typing import Literal

import httpx

from apc_hypaship.config import APCBaseModel, APCSettings
from apc_hypaship.models.request.shipment import Shipment
from apc_hypaship.models.response.label_track import Tracks
from apc_hypaship.models.response.resp import BookingResponse, ServiceAvailabilityResponse
from apc_hypaship.models.response.shipment import Label

ResponseMode = Literal['raw', 'json'] | type


class APCClient(APCBaseModel):
    """Synchronous client for the Hypaship API.

    Each method makes one blocking ``httpx`` request with a 30-second timeout. Requests are
    authenticated with the ``remote-user`` header built from :attr:`settings`.

    Example::

        client = APCClient(settings=APCSettings.from_env())
        booking = client.fetch_book_shipment(shipment)
        label = client.fetch_label(booking.order_num)
    """

    settings: APCSettings
    """Credentials and base URL used for every request."""

    def do_post(
        self,
        *,
        url: str,
        data: dict | None = None,
    ) -> httpx.Response:
        """POST ``data`` as JSON to ``url`` with auth headers.

        :raises httpx.HTTPStatusError: if the response status is 4xx/5xx.
        """
        headers = self.settings.headers
        res = httpx.post(url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        return res

    def do_get(
        self,
        *,
        url: str,
        params: dict | None = None,
    ) -> httpx.Response:
        """GET ``url`` with query ``params`` and auth headers.

        :raises httpx.HTTPStatusError: if the response status is 4xx/5xx.
        """
        headers = self.settings.headers
        res = httpx.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        return res

    def fetch_service_available(
        self,
        shipment: Shipment,
    ) -> ServiceAvailabilityResponse:
        """List the services available for ``shipment`` (``POST ServiceAvailability.json``).

        Does not raise on Hypaship business errors; check
        ``result.service_availability.messages.code``.

        :param shipment: The shipment to quote. ``product_code`` is ignored by Hypaship here.
        :returns: Available services with transit times, limits and prices.
        """
        shipment_dict = shipment.model_dump(by_alias=True, mode='json')
        res = self.do_post(url=self.settings.services_endpoint, data=shipment_dict)
        return ServiceAvailabilityResponse(**res.json())

    def fetch_book_shipment(
        self,
        shipment: Shipment,
    ) -> BookingResponse:
        """Book ``shipment`` (``POST Orders.json``).

        :param shipment: The shipment to book.
        :returns: The booking response; the new order number is at
            :attr:`BookingResponse.order_num <apc_hypaship.models.response.resp.BookingResponse.order_num>`.
        :raises APCException: if Hypaship rejects the order (e.g. invalid postcode).
        :raises ValueError: if Hypaship returns an error code not in ``error_dict``.
        :raises httpx.HTTPStatusError: on an HTTP error status.
        """
        shipment_dict = shipment.model_dump(by_alias=True, mode='json')
        res = self.do_post(url=self.settings.orders_endpoint, data=shipment_dict)
        response = BookingResponse(**res.json())
        response.raise_for_errors()
        return response

    def fetch_label(
        self,
        shipment_num: str,
        format: Literal['PDF'] = 'PDF',
    ) -> Label:
        """Fetch the label for an order (``GET Orders/{shipment_num}.json``).

        Hypaship needs a few seconds after booking to generate the label; retrying is fine.
        Fetching a label marks the order as printed.

        :param shipment_num: The 18-digit Hypaship order number.
        :param format: Label format. Only ``'PDF'`` is supported.
        :returns: The label; ``content`` is **base64-encoded** bytes.
        """
        params = {'labelformat': format}
        label = self.do_get(
            url=self.settings.one_order_endpoint(shipment_num),
            params=params,
        )
        label = BookingResponse(**label.json())
        return label.orders.order.label

    def fetch_tracks(
        self,
        shipment_num: str,
    ) -> Tracks:
        """Fetch tracking information for an order (``GET Tracks/{shipment_num}.json``).

        :param shipment_num: The 18-digit Hypaship order number.
        """
        res = self.do_get(url=self.settings.track_endpoint(shipment_num))
        res = res.json()
        t = res.get('Tracks')
        return Tracks(**t)
