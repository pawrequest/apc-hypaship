# Error handling

The client can fail in three ways.

## 1. Validation errors (before any request)

If a model is built with missing or invalid data, pydantic raises `pydantic.ValidationError`
before anything is sent. For example, a missing `delivery` or an address line over 64 characters.

## 2. HTTP errors

{meth}`~apc_hypaship.apc_client.APCClient.do_get` and
{meth}`~apc_hypaship.apc_client.APCClient.do_post` call `raise_for_status()`, so any 4xx/5xx
response raises `httpx.HTTPStatusError`. Authentication failures show up this way. If you get one,
check your credentials on the website first (see {doc}`getting-started`).

`apc_hypaship.error` has helpers for turning these into something readable:

```python
import httpx
from apc_hypaship.error import extract_http_error_message, extract_http_error_message_json

try:
    client.fetch_book_shipment(shipment)
except httpx.HTTPStatusError as e:
    print(extract_http_error_message(e))  # raw response body
    print(extract_http_error_message_json(e))  # the 'Messages' dict, e.g. {'Code': ..., 'Description': ...}
```

{func}`~apc_hypaship.error.apc_http_status_alerts` (async) wraps the same information in a list of
{class}`~apc_hypaship.error.Alert` objects, for apps that show alerts to users.

## 3. Hypaship business errors

Hypaship often returns HTTP 200 with an error inside the body, in a `Messages` block:

```json
{"Messages": {"Code": "201", "Description": "...",
              "ErrorFields": {"ErrorField": {"FieldName": "Delivery PostalCode", "ErrorMessage": "..."}}}}
```

{meth}`~apc_hypaship.apc_client.APCClient.fetch_book_shipment` calls
{meth}`BookingResponse.raise_for_errors() <apc_hypaship.models.response.resp.BookingResponse.raise_for_errors>`.
This checks the order-level messages first, because they are more specific, then the
orders-level messages. Any code other than `SUCCESS` raises
{class}`~apc_hypaship.models.response.common.APCException`:

```python
from apc_hypaship.models.response.common import APCException

try:
    booking = client.fetch_book_shipment(shipment)
except APCException as e:
    print(e)  # 'APC Message 201: ... - Delivery PostalCode: ...'
    print(e.code)  # '201'
    print(e.error_fields)  # ErrorField (or list of them)
    print(e.error_dict_message)  # 'Invalid Postcode'
```

Known codes are listed in `apc_hypaship.models.response.common.error_dict`:

| Code    | Meaning          |
|---------|------------------|
| `201`   | Invalid Postcode |
| `202`   | Invalid Date     |
| `ERROR` | General Error    |

If Hypaship returns a code that isn't in `error_dict`,
{meth}`Messages.raise_for_errors() <apc_hypaship.models.response.common.Messages.raise_for_errors>`
raises a plain `ValueError` asking for the code to be added. Add new codes to `error_dict` as you
find them.

`fetch_service_available`, `fetch_label` and `fetch_tracks` do **not** raise on business errors.
Check `.messages.code` on the result yourself.
