# Development

## Setup

```bash
uv sync                 # installs the package plus dev dependencies
uv run ruff check .     # lint
uv run ruff format .    # format (single quotes, 120 columns)
```

## Project layout

```text
src/apc_hypaship/
├── apc_client.py              APCClient - the HTTP client
├── config.py                  APCSettings, APCBaseModel, helpers
├── error.py                   Alert model and HTTP error helpers
└── models/
    ├── request/
    │   ├── address.py         Address, Contact
    │   ├── services.py        APCServiceCode enum
    │   └── shipment.py        Shipment, Order, GoodsInfo, ShipmentDetails, Item(s)
    └── response/
        ├── resp.py            BookingResponse, ServiceAvailabilityResponse
        ├── shipment.py        Order, Label, Item, Depots, ...
        ├── service.py         Service, Services, Rates, GoodsInfo
        ├── label_track.py     Tracks, Track
        ├── common.py          Messages, APCException, error_dict
        ├── address.py         lenient Address / Contact
        └── parcelspecs.py     ParcelSpecs size/weight limits
docs/
├── ref/                       upstream APC integration guide (PDF) and sample payloads
└── source/                    these docs (Sphinx + MyST)
```

## Tests

The tests run against the real Hypaship **training** API and book real test orders. You need
training credentials in an env file, pointed to by `APC_ENV`:

```bash
export APC_ENV=/path/to/training/apc.env
uv run pytest
```

The `sandbox_only` fixture skips every test unless `BASE_URL` contains `training`, so you can't
book live orders by accident. The test collection date is two days ahead, moved forward past
weekends.

## Building the docs

```bash
uv run sphinx-build -b html docs/source docs/build/html
```

`docs/build/` is git-ignored.
