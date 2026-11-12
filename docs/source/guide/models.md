# Request and response models

All models inherit from {class}`~apc_hypaship.config.APCBaseModel`, a pydantic `BaseModel` with
the following settings:

- **PascalCase aliases.** Python attributes are snake_case (`postal_code`). When serialized with
  `by_alias=True`, they become the names Hypaship expects (`PostalCode`). Both forms are accepted
  when you build a model.
- **Date/time encoding.** `date` → `DD/MM/YYYY`, `time` → `HH:MM`.
  {func}`~apc_hypaship.config.apc_date` does the same for a single date.
- **Enum values.** Enums are stored as their values, so `APCServiceCode.PARCEL_1600` serializes as
  `'APCND16'`.

## Request structure

A booking or availability request is a {class}`~apc_hypaship.models.request.shipment.Shipment`:

```text
Shipment
└── orders: Orders
    └── order: Order
        ├── collection_date        date   (required)
        ├── ready_at               time   default 09:00
        ├── closed_at              time   default 17:00
        ├── product_code           str    (required, e.g. APCServiceCode.PARCEL_1600)
        ├── reference              str    (required, your reference)
        ├── collection: Address    optional - omit to use the account's operational address
        ├── delivery:   Address    (required)
        │   └── contact: Contact
        ├── goods_info: GoodsInfo
        └── shipment_details: ShipmentDetails
            ├── number_of_pieces   int    (required)
            └── items: Items       optional - auto-filled if omitted
                └── item: [Item, ...]
```

Use {meth}`Shipment.from_order() <apc_hypaship.models.request.shipment.Shipment.from_order>` to
wrap an `Order`.

If you supply a `collection` address that doesn't exactly match the account's operational address,
Hypaship books the order as a **third-party pickup (PUR)**. PURs must be booked by 20:00 for
collection on the next working weekday.

### Defaults to watch out for

| Field                          | Default                | Note                                                                     |
|--------------------------------|------------------------|--------------------------------------------------------------------------|
| `ShipmentDetails.items`        | one `Item()` per piece | Each auto-created item weighs **12 kg**. Pass `Items` explicitly if yours differ. |
| `Item.type`                    | `'ALL'`                |                                                                          |
| `GoodsInfo.goods_value`        | `'1000'`               | Set the real value.                                                      |
| `GoodsInfo.goods_description`  | `'Radios'`             | Set the real description.                                                |
| `Address.country_code`         | `'GB'`                 |                                                                          |
| `Order.ready_at` / `closed_at` | 09:00 / 17:00          | `ready_at` must be earlier than `closed_at`.                             |

`Contact.email` has no default. You must pass it, even if only as `None`.

Always set `Address.company_name`. If you leave it out, serializing the shipment fails with
`PydanticSerializationError`.

### Explicit items

```python
from apc_hypaship.models.request.shipment import Item, Items, ShipmentDetails

details = ShipmentDetails(
    number_of_pieces=2,
    items=Items(
        item=[
            Item(weight=4.5, length=40, width=30, height=20, reference='box-1'),
            Item(weight=8.0, length=50, width=40, height=30, reference='box-2'),
        ]
    ),
)
```

### Field limits enforced by Hypaship

These come from the integration guide. The client only enforces the address-line lengths (and strips
their whitespace). Hypaship validates the rest.

| Field                 | Rule                                                    |
|-----------------------|---------------------------------------------------------|
| Company name          | < 35 characters (mandatory)                             |
| Address line 1 / 2    | < 64 characters (truncated to 30 on the printed label)  |
| City / County         | < 32 characters (city mandatory)                        |
| Country code          | ISO 3166-1 alpha-2 (mandatory)                          |
| Postcode              | Valid postcode, with a space (mandatory)                |
| Person name           | < 64 characters                                         |
| Telephone             | `0-9 ( ) + -` and spaces, 6–15 characters               |
| Mobile                | Starts `07`, `+447` or `00447`, followed by 9 digits    |
| Email                 | Valid email, < 64 characters                            |
| Safeplace             | `Allowed`, `NotAllowed` or `ConsigneeChoice`            |
| Product code          | Uppercase, valid service code                           |
| Reference             | < 35 characters                                         |
| Weight                | kg, min 0.01, max depends on tariff                     |
| Length/width/height   | cm, integer                                             |
| Goods description     | < 64 characters                                         |
| Instructions          | < 64 characters                                         |
| Number of pieces      | integer ≥ 1                                             |

## Response models

Response models live in `apc_hypaship.models.response`. Almost every field is optional and
typed as `str`, because Hypaship returns most values, including numbers and booleans, as
strings.

| Response                                                                | Returned by               |
|-------------------------------------------------------------------------|---------------------------|
| {class}`~apc_hypaship.models.response.resp.ServiceAvailabilityResponse` | `fetch_service_available` |
| {class}`~apc_hypaship.models.response.resp.BookingResponse`             | `fetch_book_shipment`     |
| {class}`~apc_hypaship.models.response.shipment.Label`                   | `fetch_label`             |
| {class}`~apc_hypaship.models.response.label_track.Tracks`               | `fetch_tracks`            |

`response.address.Address`/`Contact` and `response.service.GoodsInfo` subclass the request models
and make their fields optional, so partial data from Hypaship still parses.
