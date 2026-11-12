# Reference data

## Service codes

{class}`~apc_hypaship.models.request.services.APCServiceCode` lists the APC product codes. Pass one
as `Order.product_code`. The number suffix is the delivery deadline (10 = 10:30, 12 = 12:00,
16 = 16:00, i.e. end of day).

| Enum member                      | Code      | Service                          |
|----------------------------------|-----------|----------------------------------|
| `PARCEL_1030`                    | `APCND10` | Next day parcel by 10:30         |
| `PARCEL_1200`                    | `APCND12` | Next day parcel by 12:00         |
| `PARCEL_1600`                    | `APCND16` | Next day parcel                  |
| `SATURDAY_PARCEL_1030`           | `APCNS10` | Saturday parcel by 10:30         |
| `SATURDAY_PARCEL_1200`           | `APCNS12` | Saturday parcel by 12:00         |
| `LIQUID_SERVICE_1030/1200/1600`  | `APCLP10/12/16` | Liquids                    |
| `LIMITED_QUANTITY_1030/1200/1600`| `APCLQ10/12/16` | Limited quantity (dangerous goods) |
| `NON_CONVEYABLE_1030/1200/1600`  | `APCNC10/12/16` | Non-conveyable              |
| `SATURDAY_LIQUID_SERVICE_1030/1200` | `APCSL10/12` | Saturday liquids             |
| `SATURDAY_NON_CONVEYABLE_1030/1200` | `APCSN10/12` | Saturday non-conveyable      |
| `SATURDAY_LIMITED_QUANTITY_1030/1200` | `APCSQ10/12` | Saturday limited quantity  |
| `XS_SERVICE_1030/1200/1600`      | `APCXS10/12/16` | Extra-small (XS)            |
| `SATURDAY_XS_SERVICE_1030/1200`  | `APCSX10/12` | Saturday XS                    |
| `UNBOXED_1030/1200/1600`         | `APCUB10/12/16` | Unboxed                     |
| `SAT_UNBOXED_1030/1200/1600`     | `APCWU10/12/16` | Saturday unboxed            |
| `SECOND_CLASS_MAIL`              | `APCPOST` | 2nd class mail                   |

Which services you can use depends on your account and the shipment. Use
{meth}`~apc_hypaship.apc_client.APCClient.fetch_service_available` to find out.

## Parcel specifications

{class}`~apc_hypaship.models.response.parcelspecs.ParcelSpecs` is an enum of
{class}`~apc_hypaship.models.response.parcelspecs.ParcelSpec` size and weight limits
(cm, kg). Use it to validate parcels before booking.

| Spec                    | Code | Max L × W × H (cm) | Max kg | Max items | Notes                                   |
|-------------------------|------|--------------------|--------|-----------|-----------------------------------------|
| `MAILPACK`              | MP   | 37.5 × 29.5 × –    | 1      | 1         | Must fit provided/pre-approved packaging |
| `COURIERPACK`           | CP   | 54.5 × 45.5 × –    | 5      | 1         | Must fit provided/pre-approved packaging |
| `LIGHTWEIGHTPARCEL`     | LW   | 45 × 35 × 20       | 5      | 1         |                                         |
| `STANDARDNEXTDAYPARCEL` | ND   | 120 × 55 × 50      | 30     | 20        | 60 × 60 × 60 also OK                    |
| `NONCONVEYABLEPARCEL`   | NC   | 160 × 60 × 60      | 30     | 2         | width + height < 120 also OK            |

```python
from apc_hypaship.models.response.parcelspecs import ParcelSpecs

spec = ParcelSpecs.STANDARDNEXTDAYPARCEL.value
assert weight <= spec.max_weight
```

## Tracking status codes

From the integration guide (live system; some training codes differ, and APC may add more).

| Code | Status                     | Code | Status                          |
|------|----------------------------|------|---------------------------------|
| 1    | READY TO PRINT             | 94   | AT HUB - SECURITY               |
| 2    | OUT FOR DELIVERY           | 95   | HELD AT DEPOT                   |
| 3    | DELIVERED                  | 96   | CUSTOMER REFUSED                |
| 44   | RETURN TO SENDER           | 97   | CANCELLED                       |
| 62   | LABEL PRINTED              | 98   | COLLECTED/PICKED UP             |
| 63   | MANIFESTED                 | 99   | LEFT WITH NEIGHBOUR             |
| 69   | AT DELIVERY DEPOT          | 100  | UPDATED/RESOLVED                |
| 70   | AT HUB                     | 101  | NOT UPDATED/RESOLVED            |
| 71   | AT SENDING DEPOT           | 102  | RETURN TO DEPOT                 |
| 72   | BOOK IN REQUIRED           | 110  | ENROUTE                         |
| 73   | CHECK ADDRESS              | 112  | RETURN                          |
| 74   | COLLECTED FROM DEPOT       | 113  | BARCODE INFORMATION SCAN        |
| 75   | CUSTOMER RE-ARRANGED       | 114  | SCAN TO ROUTE                   |
| 76   | CLOSED / CARDED            | 115  | PUR Confirmed                   |
| 77   | DAMAGED                    | 116  | Collection address incorrect    |
| 79   | INTERCOM - NO ACCESS       | 117  | Collection not ready            |
| 80   | INCOMPLETE                 | 118  | Collection not required         |
| 81   | LEFT AS INSTRUCTED         | 119  | No-one present at collection    |
| 83   | NOT RECEIVED ON TRUNK      | 121  | DEPOT SORT SCAN                 |
| 84   | NOT RECEIVED IN DEPOT      | 122  | Failsafe Scan                   |
| 85   | PLANNED - NOT ATTEMPTED    | 123  | MISSCAN                         |
| 86   | QUEUE                      | 125  | PUR Not Required                |
| 88   | VEHICLE BREAKDOWN          | 126  | MISSORT                         |
| 89   | DELAYED BY WEATHER         | 145  | SCAN TO DEPOT                   |
| 92   | ORDER CREATED              | 149  | DISPOSED OF                     |
| 93   | AT DEPOT                   | 150  | HELD AWAITING COLLECTION        |
|      |                            | 151–156 | Parcelly statuses (cancelled, returned, re-direct, ready for collection, time-out, customer collected) |
