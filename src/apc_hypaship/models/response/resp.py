from apc_hypaship.config import APCBaseModel

"""Top-level response models returned by :class:`~apc_hypaship.apc_client.APCClient`."""

from apc_hypaship.models.response.common import Messages
from apc_hypaship.models.response.service import Services
from apc_hypaship.models.response.shipment import Order, Orders


class Response(APCBaseModel):
    """Base class for responses."""


class BookingResponse(Response):
    """Response from booking an order or fetching one (``Orders`` endpoints)."""

    orders: Orders | None = None

    def raise_for_errors(self):
        """Raise if the order-level or orders-level messages are not ``SUCCESS``.

        Order-level messages are checked first because they are more specific.

        :raises APCException: for known error codes.
        :raises ValueError: for unknown error codes.
        """
        # todo handle multiple errors... here we raise order errors first because more descriptive
        if self.orders and self.orders.order:
            self.orders.order.messages.raise_for_errors()
        if self.orders and self.orders.messages:
            self.orders.messages.raise_for_errors()

    @property
    def order_num(self):
        """The Hypaship order number, or ``None`` if there is no order."""
        return self.orders.order.order_number if self.orders and self.orders.order else None


class OrdersResponse(APCBaseModel):
    orders: Orders


class ServiceAvailability(APCBaseModel):
    """Body of a service-availability response."""

    account_number: str | None = None
    messages: Messages | None = None
    order: Order | None = None
    services: Services | None = None


class ServiceAvailabilityResponse(APCBaseModel):
    """Response from ``ServiceAvailability.json``."""

    service_availability: ServiceAvailability
