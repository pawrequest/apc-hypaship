"""Address and contact request models."""

# from pawdantic.paw_types import str_length_const

from apc_hypaship.config import APCBaseModel, str_length_const


class Contact(APCBaseModel):
    """Contact person at an address.

    Hypaship expects mobile numbers to start with ``07``, ``+447`` or ``00447``. ``email`` has no
    default, so you must pass it, even if only as ``None``.
    """

    person_name: str
    phone_number: str | None = None
    mobile_number: str
    email: str | None


class Address(APCBaseModel):
    """A collection or delivery address.

    Address lines are stripped and limited to 64 characters. Postcodes need a space
    (e.g. ``NW2 3EJ``). ``safeplace`` may be ``Allowed``, ``NotAllowed`` or ``ConsigneeChoice``.
    """

    contact: Contact
    company_name: str = str_length_const(34)
    address_line_1: str_length_const(64)
    address_line_2: str_length_const(64) | None = None
    city: str
    county: str | None = None
    postal_code: str
    country_code: str = 'GB'
    country_name: str | None = None
    instructions: str | None = None
    safeplace: str | None = None


class AddressDelivery(Address):
    """Delivery address with ``instructions`` defaulting to an empty string."""

    instructions: str = ''
