# apc-hypaship

A small, typed Python client for the APC Overnight **Hypaship** booking platform API (v3).

It wraps the Hypaship JSON endpoints with [httpx](https://www.python-httpx.org/) and
[pydantic](https://docs.pydantic.dev/) models. You build a shipment as Python objects and get
validated, typed responses back.

| Operation                  | Client method                                                     | Hypaship endpoint                |
|----------------------------|-------------------------------------------------------------------|----------------------------------|
| Check service availability | {meth}`~apc_hypaship.apc_client.APCClient.fetch_service_available` | `POST ServiceAvailability.json`  |
| Book a shipment            | {meth}`~apc_hypaship.apc_client.APCClient.fetch_book_shipment`     | `POST Orders.json`               |
| Retrieve a label           | {meth}`~apc_hypaship.apc_client.APCClient.fetch_label`             | `GET Orders/{order_number}.json` |
| Track an order             | {meth}`~apc_hypaship.apc_client.APCClient.fetch_tracks`            | `GET Tracks/{order_number}.json` |

Amending and cancelling orders are not implemented yet.

The upstream reference is the *APC API v3 Integration Guide* (edition 3.1.2), kept in the
repository at `docs/ref/APC_API_Integration_Guide_V3.1.2.pdf`.

```{toctree}
:maxdepth: 2
:caption: Guide

guide/getting-started
guide/workflow
guide/models
guide/errors
guide/reference-data
guide/development
```

```{toctree}
:maxdepth: 2
:caption: API reference

api
```
