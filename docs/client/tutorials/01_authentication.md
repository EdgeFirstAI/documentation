# Tutorial 1: Authentication

Verify that the Python API shares the same authentication token as the `edgefirst-client` CLI.

**CLI equivalent:** `login`, `logout`, `token`

## Prerequisites

- `pip install edgefirst-client`
- Run `edgefirst-client login` once, or set `STUDIO_TOKEN`

## Steps

### 1. Log in with the CLI

```bash
edgefirst-client login
```

The token is cached at the platform default path (see [CLI authentication](../cli/index.md#authentication)).

### 2. Create a client from the cached token

```python
from edgefirst_client import FileTokenStorage
from examples import get_client, token_storage_path

print("Token file:", token_storage_path())

client = get_client()
client.verify_token()

print("Server URL:", client.url)
print("Username:", client.username())
print("Token expires:", client.token_expiration)
```

`get_client()` checks `STUDIO_TOKEN`, then `STUDIO_USERNAME` / `STUDIO_PASSWORD`, then falls back to the CLI-cached token via `Client()`.

### 3. Optionally renew the token

```python
try:
    client.renew_token()
    print("Token renewed successfully.")
except Exception as exc:
    print("Token renew skipped or failed:", exc)
```

## Expected output

```text
Token file: /home/user/.config/EdgeFirst Studio/token
Server URL: https://edgefirst.studio
Username: your@email.com
Token expires: ...
Authentication OK.
```

## Source

Full script: [01_authentication.py](https://github.com/EdgeFirstAI/client/blob/main/examples/01_authentication.py)

---

**Next:** [Tutorial 2: Explore dataset](02_explore_dataset.md)
