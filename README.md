# SpeedtestTrackerAPI

A modern, type-safe, and async-friendly Python API wrapper for the **[Speedtest Tracker]([https://github.com/alexjustesen/speedtest-tracker])** (a self-hosted Docker container for automated internet speedtests).

> ⚠️ **Important Note:** This package is an **unofficial community project** and is not officially affiliated with or endorsed by the original *Speedtest Tracker* project or its developers.

---

## Features

- ✨ **Full IDE Support:** Complete auto-completion (IntelliSense) powered by native `Pydantic v2` models.
- 🛡️ **Built-in Validation:** Erroneous filter values or invalid data types are caught locally before an invalid request is ever sent to your API.
- 🔒 **Secure SSL Control:** Flexible option to skip SSL verification (`verify_ssl=False`) for local IP addresses or self-signed certificates within Docker networks.
- 📦 **Comprehensive Error Handling:** Dedicated, descriptive exception classes for authentication failures, missing endpoints, or network errors.

---

## Installation

Install the package easily using your preferred Python package management tool:

```bash
# Using uv (recommended)
uv add speedtest-tracker-api

# Or using classic pip
pip install speedtest-tracker-api
```

---

## Quickstart

To connect to your local *Speedtest Tracker* Docker container, you will need the container's **base URL** and an **API token** with at least results:read ability to get speedtest results.

```python
from speedtesttrackerapi import ApiClient, ApiError
from pydantic import ValidationError

# 1. Initialize the API client
# For local Docker containers, you can disable SSL verification if needed
client = ApiClient(
    base_url="http://localhost:8080",
    token="1|pAasdfM...YOUR_ACTUAL_API_TOKEN",
    verify_ssl=False
)

try:
    print("Fetching speedtest results...")
    
    # 2. Query results:
    results = client.get_results()
    
    # 3. Use data fully type-safe (with auto-completion in VS Code/PyCharm)
    print(f"\nFound {len(results.data)} matching results:")
    for e in results.data:
        print(f"[{e.created_at}] ID: {e.id}")
        print(f"  ⬇️ Download: {e.download_human_bits}")
        print(f"  ⬆️ Upload:   {e.upload_human_bits}")
        print(f"  ⏱️ Ping:     {e.ping} ms")
        print("-" * 30)

except ValidationError as e:
    print(f"Input Error: Your input was invalid: {e}")
except ApiError as e:
    print(f"API Error occurred: {e}")
```

---

## Error Handling

The package provides specific exceptions to handle issues during API communication gracefully:

```python
from speedtesttrackerapi import ApiError, AuthenticationError, ResourceNotFoundError

try:
    results = client.get_results()
except AuthenticationError:
    print("Error: Your API token is invalid or expired!")
except ResourceNotFoundError:
    print("Error: The specified API endpoint was not found on the server.")
except ApiError as e:
    print(f"General network or connection error: {e}")
```

---

## Development & Contributing

Since this project is managed with **`uv`**, setting up the local development environment is extremely straightforward:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mx-fschr/SpeedtestTrackerAPI.git
   cd SpeedtestTrackerAPI
   ```
2. **Create virtual environment and install dependencies:**
   ```bash
   uv sync
   ```
3. **Run tests:**
   The project uses `pytest` and `responses`. You can run the test suite locally without accessing a live API:
   ```bash
   uv run pytest -s
   ```

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
