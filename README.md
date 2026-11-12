# apc-hypaship

A small, typed Python client for the [APC Overnight](https://apc-overnight.com) **Hypaship** booking platform API (v3).

It wraps the JSON endpoints of the Hypaship API with [httpx](https://www.python-httpx.org/) and
[pydantic](https://docs.pydantic.dev/) models, so you can build shipments as Python objects
and get validated, typed responses back.

Supported operations:

| Operation                  | Client method                              | Hypaship endpoint                    |
|----------------------------|--------------------------------------------|--------------------------------------|
| Check service availability | `APCClient.fetch_service_available()`      | `POST ServiceAvailability.json`      |
| Book a shipment (order)    | `APCClient.fetch_book_shipment()`          | `POST Orders.json`                   |
| Retrieve a label           | `APCClient.fetch_label()`                  | `GET Orders/{order_number}.json`     |
| Track an order             | `APCClient.fetch_tracks()`                 | `GET Tracks/{order_number}.json`     |

Amending and cancelling orders are not implemented yet.

The upstream API reference (*APC API v3 Integration Guide, edition 3.1.2*) is in
[`docs/ref/APC_API_Integration_Guide_V3.1.2.pdf`](docs/ref/APC_API_Integration_Guide_V3.1.2.pdf).

---

## Installation

Requires Python **3.13+**.

```bash
uv add apc-hypaship
# or
pip install apc-hypaship
```

## Configuration

Credentials and the API base URL come from an env file, loaded by `APCSettings`
(a [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) class).

```ini
# apc.env
APC_EMAIL=you@example.com
APC_PASSWORD=your-hypaship-password
BASE_URL=https://apc-training.hypaship.com/api/3.0/
```

| Variable       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `APC_EMAIL`    | Hypaship login email. Training and live use separate credentials.           |
| `APC_PASSWORD` | Hypaship login password.                                                    |
| `BASE_URL`     | API root URL. **Must end with `/`**, because endpoint paths are appended to it. |

| Environment | `BASE_URL`                                    | Website                             |
|-------------|-----------------------------------------------|-------------------------------------|
| Training    | `https://apc-training.hypaship.com/api/3.0/`  | https://apc-training.hypaship.com   |
| Live        | `https://apc.hypaship.com/api/3.0/`           | https://apc.hypaship.com            |

There are three ways to load settings:

```python
from pathlib import Path
from apc_hypaship.config import APCSettings

# 1. From an env var that holds the path to the env file (default var name: APC_ENV)
#    e.g. APC_ENV=/path/to/apc.env
settings = APCSettings.from_env()  # or APCSettings.from_env('MY_VAR')

# 2. From an explicit env-file path
settings = APCSettings.from_env_file(Path('apc.env'))

# 3. Directly (or from process environment variables)
settings = APCSettings(apc_email='...', apc_password='...', base_url='https://apc-training.hypaship.com/api/3.0/')
```

The client authenticates every request with the `remote-user: Basic base64(email:password)` header
required by Hypaship. `APCSettings.headers` builds it for you.

## Quick start

```python
import base64
from datetime import date
from pathlib import Path

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
        contact=Contact(person_name='Jane Doe', mobile_number='07700900000', email='jane@example.com'),
    ),
    goods_info=GoodsInfo(goods_value='250', goods_description='Radios'),
    shipment_details=ShipmentDetails(number_of_pieces=2),
)
shipment = Shipment.from_order(order)

# 1. (optional) see which services are available for this shipment
availability = client.fetch_service_available(shipment)
for svc in availability.service_availability.services.service:
    print(svc.product_code, svc.service_name, svc.total_cost)

# 2. book it - raises APCException if Hypaship rejects the order
booking = client.fetch_book_shipment(shipment)
order_num = booking.order_num

# 3. fetch the label (allow a few seconds after booking for it to be generated)
label = client.fetch_label(order_num)
Path(f'{order_num}.pdf').write_bytes(base64.b64decode(label.content))

# 4. track it
tracks = client.fetch_tracks(order_num)
print(tracks.messages.code, tracks.track.way_bill)
```

### Things to know

- **Field names**: models use snake_case in Python and serialize to the PascalCase names Hypaship
  expects (`postal_code` → `PostalCode`). Either form is accepted when constructing models.
- **Dates and times** are sent as `DD/MM/YYYY` and `HH:MM`.
- **Collection address**: if `Order.collection` is omitted, Hypaship uses the account's operational
  address. If you supply one that doesn't exactly match it, the order becomes a *third-party pickup (PUR)*.
- **Items**: if `ShipmentDetails.items` is omitted, one `Item` per piece is created automatically,
  each with a **default weight of 12 kg**. Pass explicit `Items` if your parcels differ.
- **Labels** are returned base64-encoded in `Label.content`; decode before writing to disk.
  Only PDF is currently supported by `fetch_label`.
- **Errors**: HTTP errors raise `httpx.HTTPStatusError`. Business errors on booking
  (e.g. invalid postcode) raise `apc_hypaship.models.response.common.APCException`,
  which carries `code` and `error_fields`.

## Documentation

Full docs (guides + API reference generated from the source) are built with Sphinx:

```bash
uv sync
uv run sphinx-build -b html docs/source docs/build/html
```

Then open `docs/build/html/index.html`.

## Development

```bash
uv sync                 # install with dev dependencies
uv run ruff check .     # lint
uv run ruff format .    # format
```

### Tests

The tests hit the real Hypaship **training** API (they book real test orders), so you need
training credentials:

```bash
export APC_ENV=/path/to/training/apc.env
uv run pytest
```

As a safety net, the tests are skipped unless `BASE_URL` contains `training`.
