# Booking workflow

The Hypaship workflow has four steps. Service availability is optional; the rest are the normal
path for getting a shipment out of the door.

```text
1. Check service availability   (optional)   POST ServiceAvailability.json
2. Book the order                (required)   POST Orders.json
   ... wait a few seconds for the label to be generated ...
3. Fetch the label               (required)   GET  Orders/{order_number}.json?labelformat=PDF
4. Track the order               (any time)   GET  Tracks/{order_number}.json
```

All examples below use this shipment:

```python
from datetime import date

from apc_hypaship.apc_client import APCClient
from apc_hypaship.config import APCSettings
from apc_hypaship.models.request.address import Address, Contact
from apc_hypaship.models.request.services import APCServiceCode
from apc_hypaship.models.request.shipment import GoodsInfo, Order, Shipment, ShipmentDetails

client = APCClient(settings=APCSettings.from_env())

order = Order(
    collection_date=date(2026, 11, 16),
    product_code=APCServiceCode.PARCEL_1600,
    reference='ORDER-1234',
    delivery=Address(
        company_name='Acme Ltd',
        address_line_1='1 High Street',
        city='London',
        postal_code='NW2 3EJ',
        contact=Contact(
            person_name='Jane Doe',
            mobile_number='07700900000',
            email='jane@example.com',
        ),
    ),
    goods_info=GoodsInfo(goods_value='250', goods_description='Radios'),
    shipment_details=ShipmentDetails(number_of_pieces=1),
)
shipment = Shipment.from_order(order)
```

## 1. Check service availability

{meth}`~apc_hypaship.apc_client.APCClient.fetch_service_available` sends the shipment to
`ServiceAvailability.json`. It returns every service that can carry it, with transit times, size
limits and prices.

```python
res = client.fetch_service_available(shipment)
for svc in res.service_availability.services.service:
    print(svc.product_code, svc.service_name, svc.estimated_delivery_date, svc.total_cost)
```

The result is a {class}`~apc_hypaship.models.response.resp.ServiceAvailabilityResponse`. Each
{class}`~apc_hypaship.models.response.service.Service` has a `product_code` that you can use as
`Order.product_code` when booking.

This method does **not** call `raise_for_errors()`. Check
`res.service_availability.messages.code` yourself if you need to tell an empty result apart from an
error.

## 2. Book the order

{meth}`~apc_hypaship.apc_client.APCClient.fetch_book_shipment` posts the shipment to `Orders.json`
and returns a {class}`~apc_hypaship.models.response.resp.BookingResponse`.

```python
booking = client.fetch_book_shipment(shipment)
print(booking.order_num)                       # 18-digit order number
print(booking.orders.order.way_bill)           # 22-digit carrier waybill
```

If Hypaship rejects the order (for example, an invalid postcode), the method raises
{class}`~apc_hypaship.models.response.common.APCException`. See {doc}`errors`.

## 3. Fetch the label

Hypaship needs a few seconds after booking to generate the label. If you ask for it too early, it
is fine to retry.

```python
import base64
import time
from pathlib import Path

time.sleep(3)
label = client.fetch_label(booking.order_num)
Path(f'{booking.order_num}.pdf').write_bytes(base64.b64decode(label.content))
```

{meth}`~apc_hypaship.apc_client.APCClient.fetch_label` returns a
{class}`~apc_hypaship.models.response.shipment.Label`. `content` holds the **base64-encoded**
label as `bytes`, so decode it before you save it. Only `PDF` is supported for now. The Hypaship
API also offers `PNG` and `ZPL`.

The lookup is by order number, which is Hypaship's default `searchtype`. Fetching a label marks the
order as printed in Hypaship.

## 4. Track the order

```python
tracks = client.fetch_tracks(booking.order_num)
print(tracks.messages.code)          # 'SUCCESS'
print(tracks.track.way_bill)
print(tracks.track.depots)
```

{meth}`~apc_hypaship.apc_client.APCClient.fetch_tracks` returns a
{class}`~apc_hypaship.models.response.label_track.Tracks` object. Tracking status codes are listed
in {doc}`reference-data`.

## Low-level requests

For endpoints the client doesn't wrap yet, use
{meth}`~apc_hypaship.apc_client.APCClient.do_get` and
{meth}`~apc_hypaship.apc_client.APCClient.do_post`. They add the auth headers, call
`raise_for_status()` and return the raw `httpx.Response`.

```python
res = client.do_get(
    url=client.settings.one_order_endpoint(booking.order_num),
    params={'searchtype': 'OrderNumber', 'labelformat': 'ZPL'},
)
raw = res.json()
```
