# Getting started

## Installation

Requires Python **3.13+**.

```bash
uv add apc-hypaship
# or
pip install apc-hypaship
```

## Credentials and environments

Hypaship has two environments. Each has its own credentials. Your API login is the same as your
website login, so the quickest way to check credentials is to log in to the website.

| Environment | API base URL                                  | Website                           |
|-------------|-----------------------------------------------|-----------------------------------|
| Training    | `https://apc-training.hypaship.com/api/3.0/`  | https://apc-training.hypaship.com |
| Live        | `https://apc.hypaship.com/api/3.0/`           | https://apc.hypaship.com          |

URLs are case sensitive.

## Settings

{class}`~apc_hypaship.config.APCSettings` holds the credentials and base URL. It is a
pydantic-settings class, so values can come from keyword arguments, process environment variables
or an env file.

```ini
# apc.env
APC_EMAIL=you@example.com
APC_PASSWORD=your-hypaship-password
BASE_URL=https://apc-training.hypaship.com/api/3.0/
```

`BASE_URL` **must end with a `/`**. Endpoint paths such as `Orders.json` are appended to it as-is.

### Loading settings

```python
from pathlib import Path
from apc_hypaship.config import APCSettings

# From an env var holding the *path* to an env file (defaults to APC_ENV).
settings = APCSettings.from_env()          # reads $APC_ENV
settings = APCSettings.from_env('MY_VAR')  # reads $MY_VAR

# From an explicit env-file path.
settings = APCSettings.from_env_file(Path('apc.env'))

# Directly.
settings = APCSettings(
    apc_email='you@example.com',
    apc_password='secret',
    base_url='https://apc-training.hypaship.com/api/3.0/',
)
```

{meth}`~apc_hypaship.config.APCSettings.from_env` is cached (`lru_cache`), so repeated calls with
the same variable name return the same settings object. It raises `ValueError` if the variable is
unset or points to a file that doesn't exist.

The email and password are stored as `SecretStr`, so they don't show up in reprs or logs.

## Authentication

Every request sends these headers, built by {attr}`~apc_hypaship.config.APCSettings.headers`:

```text
Content-Type: application/json
remote-user: Basic <base64("email:password")>
```

## Creating a client

```python
from apc_hypaship.apc_client import APCClient

client = APCClient(settings=settings)
```

The client has no state other than its settings. Each call makes one synchronous httpx request
with a 30-second timeout. Next, see {doc}`workflow`.
