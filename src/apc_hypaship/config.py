"""Settings, the shared pydantic base model and small helpers."""

import base64
import os
from datetime import date, time
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Self

from loguru import logger
from pydantic import AliasGenerator, BaseModel, ConfigDict, SecretStr, StringConstraints
from pydantic.alias_generators import to_pascal
from pydantic_settings import BaseSettings, SettingsConfigDict


def encode_b64_str(s: str) -> str:
    """Base64-encode a UTF-8 string."""
    return base64.b64encode(s.encode('utf8')).decode('utf8')


def get_remote_user(login, password) -> str:
    """Build the ``remote-user`` header value: ``Basic base64(login:password)``."""
    usr_str = f'{login}:{password}'
    return f'Basic {encode_b64_str(usr_str)}'


def apc_date(d: date) -> str:
    """Format a date as Hypaship expects (``DD/MM/YYYY``)."""
    return d.strftime('%d/%m/%Y')


def get_env(env_name: str = 'APC_ENV') -> Path:
    """Return the env-file path stored in the environment variable ``env_name``.

    :raises ValueError: if the variable is unset or the path does not exist.
    """
    env = os.getenv(env_name)
    if not env:
        raise ValueError(f'{env_name} not set')
    env_path = Path(env)
    if not env_path.exists():
        raise ValueError(f'{env_path} not a valid path')
    logger.debug(f'Loading environment from {env_path}')
    return env_path


class APCSettings(BaseSettings):
    """Hypaship credentials and API location.

    Values can come from keyword arguments, environment variables (``APC_EMAIL``,
    ``APC_PASSWORD``, ``BASE_URL``) or an env file.
    """

    apc_email: SecretStr
    """Hypaship login email."""
    apc_password: SecretStr
    """Hypaship login password."""
    base_url: str
    """API root, e.g. ``https://apc-training.hypaship.com/api/3.0/``. Must end with ``/``."""
    model_config = SettingsConfigDict()

    @classmethod
    @lru_cache
    def from_env(cls, env_name='APC_ENV') -> Self:
        """Load settings from the env file whose path is in the variable ``env_name``.

        Results are cached per ``env_name``.
        """
        return cls(_env_file=get_env(env_name))

    @classmethod
    def from_env_file(cls, env_path: Path) -> Self:
        """Load settings from the env file at ``env_path``."""
        return cls(_env_file=env_path)

    @property
    def headers(self) -> dict:
        """Request headers: JSON content type and ``remote-user`` basic auth."""
        usr = self.apc_email.get_secret_value()
        pwd = self.apc_password.get_secret_value()
        return {
            'Content-Type': 'application/json',
            'remote-user': get_remote_user(usr, pwd),
        }

    @property
    def services_endpoint(self) -> str:
        """URL of the service-availability endpoint."""
        return self.base_url + 'ServiceAvailability.json'

    @property
    def orders_endpoint(self) -> str:
        """URL of the order-booking endpoint."""
        return self.base_url + 'Orders.json'

    def one_order_endpoint(self, order_num: str) -> str:
        """URL of a single order (used to fetch labels)."""
        return self.base_url + f'Orders/{order_num}.json'

    def track_endpoint(self, order_num: str) -> str:
        """URL of the tracking endpoint for an order."""
        return self.base_url + f'Tracks/{order_num}.json'


class APCBaseModel(BaseModel):
    """Base for all models.

    Fields serialize to PascalCase aliases (``postal_code`` -> ``PostalCode``) and accept either
    name on input. Dates encode as ``DD/MM/YYYY``, times as ``HH:MM``, and enums are stored as
    their values.
    """

    model_config = ConfigDict(
        json_encoders={
            time: lambda v: v.strftime('%H:%M'),
            date: lambda v: v.strftime('%d/%m/%Y'),
        },
        alias_generator=AliasGenerator(
            alias=to_pascal,
        ),
        populate_by_name=True,
        use_enum_values=True,
    )


def str_length_const(length: int):
    """Return an annotated ``str`` type with whitespace stripped and a max length of ``length``."""
    return Annotated[
        str,
        StringConstraints(strip_whitespace=True, max_length=length),
    ]
