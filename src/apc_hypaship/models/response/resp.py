import pprint

from loguru import logger

from apc_hypaship.config import APCBaseModel
from apc_hypaship.models.response.common import Messages
from apc_hypaship.models.response.service import Services
from apc_hypaship.models.response.shipment import Orders, Order


class Response(APCBaseModel): ...


class BookingResponse(Response):
    orders: Orders | None = None

    @property
    def order_num(self):
        return self.orders.order.order_number if self.orders and self.orders.order else None

    @property
    def has_errors(self) -> bool:
        # todo this is likely broken. was using raw json with 'ErrorFields' but they are not in pydantic model?
        try:
            logger.warning(
                f'Checking for errors in response, likely borked\n{pprint.pformat(self.model_dump())}'
            )
            messages = self.orders.order.messages
            return hasattr(messages, 'ErrorFields')
        except (AttributeError, KeyError):
            ...
        return False


class OrdersResponse(APCBaseModel):
    orders: Orders


class ServiceAvailability(APCBaseModel):
    account_number: str | None = None
    messages: Messages | None = None
    order: Order | None = None
    services: Services | None = None


class ServiceAvailabilityResponse(APCBaseModel):
    service_availability: ServiceAvailability

