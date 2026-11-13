"""Status messages and errors shared by Hypaship responses."""

from apc_hypaship.config import APCBaseModel

error_dict = {
    '201': 'Invalid Postcode',
    '202': 'Invalid Date',
    'ERROR': 'General Error',
}
"""Known Hypaship error codes. :meth:`Messages.raise_for_errors` raises ``ValueError`` for codes not listed here."""


class APCException(Exception):
    """Raised when Hypaship returns a non-``SUCCESS`` message code.

    :ivar code: The Hypaship error code, e.g. ``'201'``.
    :ivar error_fields: The offending :class:`ErrorField` (or list of them), if any.
    :ivar error_dict_message: Short description from :data:`error_dict`.
    """

    def __init__(self, message, code=None, error_fields=None):
        super().__init__(message)
        self.code = code
        self.error_fields = error_fields
        self.error_dict_message = error_dict.get(code, 'Unknown error code')


class ErrorField(APCBaseModel):
    """A field that failed Hypaship validation."""

    field_name: str | None = None
    error_message: str | None = None


class ErrorFields(APCBaseModel):
    """One or more invalid fields."""

    error_field: ErrorField | list[ErrorField] | None = None


class Messages(APCBaseModel):
    """Status block returned by Hypaship (``Code`` is ``SUCCESS`` on success)."""

    code: str | None = None
    description: str | None = None
    error_fields: ErrorFields | None = None

    def raise_for_errors(self):
        """Do nothing on ``SUCCESS``; otherwise raise.

        :raises APCException: for codes listed in :data:`error_dict`.
        :raises ValueError: for unknown codes.
        """
        if self.code == 'SUCCESS':
            return
        if self.code not in error_dict:
            raise ValueError(f'Unknown error code: {self.code} Please add to dictionary.')
        msg = 'APC Message'
        msg += f' {self.code}' if self.code else ''
        msg += f': {self.description}' if self.description else ''
        if self.error_fields:
            if ef := self.error_fields.error_field:
                msg += f' - {ef.field_name}: {ef.error_message}'
        raise APCException(
            msg,
            code=self.code,
            error_fields=self.error_fields.error_field if self.error_fields else None,
        )
