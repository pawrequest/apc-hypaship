"""Request models for booking and service-availability calls."""

from datetime import date, time
from typing import Literal
from collections.abc import Sequence

from pydantic import Field, model_validator
from loguru import logger

from apc_hypaship.models.request.address import Address
from apc_hypaship.config import APCBaseModel


class Item(APCBaseModel):
    """A single piece in a shipment. Weight is in kg; dimensions are in cm."""

    type: Literal['ALL'] = 'ALL'
    weight: float | None = 12
    length: float | None = None
    width: float | None = None
    height: float | None = None
    reference: str | None = None


class Items(APCBaseModel):
    """Container for the items in a shipment."""

    item: Sequence[Item] = Field(default_factory=list)


class ShipmentDetails(APCBaseModel):
    """Number of pieces and their details.

    If ``items`` is omitted, one default :class:`Item` (12 kg) is created per piece.
    """

    number_of_pieces: int
    items: Items | None = None

    @model_validator(mode='after')
    def check_items(self):
        """Create default items if none were given."""
        if not self.items:
            self.items = Items(item=[Item() for _ in range(self.number_of_pieces)])
            logger.debug('Auto-filled items with weight = 12kg per box')
        return self


class GoodsInfo(APCBaseModel):
    """Description, value and handling options for the goods.

    Defaults are placeholders. Set ``goods_value`` and ``goods_description`` for real shipments.
    """

    goods_value: str = '1000'
    goods_description: str = 'Radios'
    fragile: bool = False
    security: bool = False
    increased_liability: bool = False
    premium_insurance: bool = False
    premium: bool = False


class Order(APCBaseModel):
    """A single order: when, what service, where from and to, and what is being sent.

    If ``collection`` is omitted, Hypaship uses the account's operational address. A collection
    address that doesn't match it makes the order a third-party pickup (PUR).
    """

    collection_date: date
    ready_at: time = time(hour=9)
    closed_at: time = time(hour=17)
    product_code: str
    """APC service code, e.g. :attr:`APCServiceCode.PARCEL_1600 <apc_hypaship.models.request.services.APCServiceCode.PARCEL_1600>`."""
    reference: str
    """Your own reference (< 35 characters)."""
    collection: Address | None = None
    delivery: Address
    goods_info: GoodsInfo
    shipment_details: ShipmentDetails


class Orders(APCBaseModel):
    """Wrapper required by the Hypaship request schema."""

    order: Order


class Shipment(APCBaseModel):
    """Top-level request body for ``ServiceAvailability`` and ``Orders``."""

    orders: Orders

    @classmethod
    def from_order(cls, order: Order) -> 'Shipment':
        """Wrap a single :class:`Order` in a ``Shipment``."""
        return cls(orders=Orders(order=order))
