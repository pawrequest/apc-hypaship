# from typing import List, Union
#
# from apc_hypaship.config import APCBaseModel
#
#
# class Contact(APCBaseModel):
#     email: str | None = None
#     person_name: str | None = None
#     phone_number: str | None = None
#     mobile_number: str | None = None
#
#
# class Address(APCBaseModel):
#     address_line1: str | None = None
#     address_line2: str | None = None
#     city: str | None = None
#     company_name: str | None = None
#     contact: Contact | None = None
#     country_code: str | None = None
#     country_name: str | None = None
#     county: str | None = None
#     instructions: str | None = None
#     postal_code: str | None = None
#     safeplace: str | None = None
#
#
# class Depots(APCBaseModel):
#     collecting_depot: str | None = None
#     delivery_depot: str | None = None
#     delivery_route: str | None = None
#     is_scottish: str | None = None
#     presort: str | None = None
#     request_depot: str | None = None
#     route: str | None = None
#     seg_code: str | None = None
#     zone: str | None = None
#
#
# class GoodsInfo(APCBaseModel):
#     charge_on_delivery: str | None = None
#     fragile: str | None = None
#     goods_description: str | None = None
#     goods_value: str | None = None
#     increased_liability: str | None = None
#     non_conv: str | None = None
#     premium: str | None = None
#     premium_insurance: str | None = None
#     security: str | None = None
#
#
# class Rates(APCBaseModel):
#     currency: str | None = None
#     extra_charges: str | None = None
#     fuel_charge: str | None = None
#     insurance_charge: str | None = None
#     rate: str | None = None
#     total_cost: str | None = None
#     vat: str | None = None
#
#
# class Item(APCBaseModel):
#     height: str | None = None
#     item_number: str | None = None
#     length: str | None = None
#     reference: str | None = None
#     tracking_number: str | None = None
#     "type: str | None = None"
#     value: str | None = None
#     weight: str | None = None
#     width: str | None = None
#
#
# class ShipmentDetails(APCBaseModel):
#     items: Union[Item, List[Item]] | None = None
#     number_of_pieces: str | None = None
#     total_weight: str | None = None
#     volumetric_weight: str | None = None
#
#
# class Messages(APCBaseModel):
#     code: str | None = None
#     description: str | None = None
#
#
# class Order(APCBaseModel):
#     account_number: List[str] | None = None
#     adult_signature: str | None = None
#     barcode: str | None = None
#     closed_at: str | None = None
#     collection: Address | None = None
#     collection_date: str | None = None
#     custom_reference1: str | None = None
#     custom_reference2: str | None = None
#     custom_reference3: str | None = None
#     delivery: Address | None = None
#     delivery_date: str | None = None
#     depots: Depots | None = None
#     entry_type: str | None = None
#     goods_info: GoodsInfo | None = None
#     item_option: str | None = None
#     messages: Messages | None = None
#     network_name: str | None = None
#     order_number: str | None = None
#     product_code: str | None = None
#     rates: Rates | None = None
#     ready_at: str | None = None
#     reference: str | None = None
#     rule_name: str | None = None
#     shipment_details: ShipmentDetails | None = None
#     way_bill: str | None = None
#
#
# class Orders(APCBaseModel):
#     account_number: str | None = None
#     messages: Messages | None = None
#     order: Order | None = None
#
#
# class ShipmentBookingResponse(APCBaseModel):
#     orders: Orders | None = None
#
#     @property
#     def order_num(self):
#         return self.orders.order.order_number if self.orders and self.orders.order else None


from typing import List, Union

import httpx
from pydantic import field_validator

from apc_hypaship.config import APCBaseModel


class Contact(APCBaseModel):
    email: str | None = None
    person_name: str | None = None
    phone_number: str | None = None
    mobile_number: str | None = None


class Address(APCBaseModel):
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    company_name: str | None = None
    contact: Contact | None = None
    country_code: str | None = None
    country_name: str | None = None
    county: str | None = None
    instructions: str | None = None
    postal_code: str | None = None
    safeplace: str | None = None


class Depots(APCBaseModel):
    collecting_depot: str | None = None
    delivery_depot: str | None = None
    delivery_route: str | None = None
    is_scottish: str | None = None
    presort: str | None = None
    request_depot: str | None = None
    route: str | None = None
    seg_code: str | None = None
    zone: str | None = None


class GoodsInfo(APCBaseModel):
    charge_on_delivery: str | None = None
    fragile: str | None = None
    goods_description: str | None = None
    goods_value: str | None = None
    increased_liability: str | None = None
    non_conv: str | None = None
    premium: str | None = None
    premium_insurance: str | None = None
    security: str | None = None


class Rates(APCBaseModel):
    currency: str | None = None
    extra_charges: str | None = None
    fuel_charge: str | None = None
    insurance_charge: str | None = None
    rate: str | None = None
    total_cost: str | None = None
    vat: str | None = None


class Label(APCBaseModel):
    content: bytes | None = None
    format: str | None = None


class Item(APCBaseModel):
    height: str | None = None
    item_number: str | None = None
    length: str | None = None
    reference: str | None = None
    tracking_number: str | None = None
    type: str | None = None
    value: str | None = None
    weight: str | None = None
    width: str | None = None
    label: Label | None = None


class ShipmentDetails(APCBaseModel):
    items: Union[Item, List[Item]] | None = None
    number_of_pieces: str | None = None
    total_weight: str | None = None
    volumetric_weight: str | None = None


class Messages(APCBaseModel):
    code: str | None = None
    description: str | None = None


class Order(APCBaseModel):
    account_number: List[str] | None = None
    adult_signature: str | None = None
    barcode: str | None = None
    closed_at: str | None = None
    collection: Address | None = None
    collection_date: str | None = None
    custom_reference1: str | None = None
    custom_reference2: str | None = None
    custom_reference3: str | None = None
    delivery: Address | None = None
    delivery_date: str | None = None
    depots: Depots | None = None
    entry_type: str | None = None
    goods_info: GoodsInfo | None = None
    item_option: str | None = None
    label: Label | None = None
    messages: Messages | None = None
    network_name: str | None = None
    order_number: str | None = None
    product_code: str | None = None
    rates: Rates | None = None
    ready_at: str | None = None
    reference: str | None = None
    rule_name: str | None = None
    shipment_details: ShipmentDetails | None = None
    way_bill: str | None = None


class Orders(APCBaseModel):
    account_number: str | None = None
    messages: Messages | None = None
    order: Order | None = None


class Response(APCBaseModel): ...


class BookingResponse(Response):
    orders: Orders | None = None

    @property
    def order_num(self):
        return (
            self.orders.order.order_number
            if self.orders and self.orders.order
            else None
        )

# class LabelResponse(Response):

ResponseType = BookingResponse | dict | httpx.Response


class Track(APCBaseModel):
    adult_signature: str | None = None
    closed_at: str | None = None
    collection: Address | None = None
    collection_date: str | None = None
    custom_reference1: str | None = None
    custom_reference2: str | None = None
    custom_reference3: str | None = None
    delivery: Address | None = None
    depots: Depots | None = None
    goods_info: GoodsInfo | None = None
    item_option: str | None = None
    order_number: str | None = None
    product_code: str | None = None
    ready_at: str | None = None
    reference: str | None = None
    shipment_details: ShipmentDetails | None = None
    way_bill: str | None = None


class Tracks(APCBaseModel):
    account_number: str | None = None
    messages: Messages | None = None
    track: Track | None = None
