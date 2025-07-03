"""Simple uploader for documents to Vectara.

Reads a JSON file containing documents and sends them to Vectara's
``/v1/upload`` endpoint.  Credentials come from ``VECTARA_CUSTOMER_ID``,
``VECTARA_CORPUS_ID`` and ``VECTARA_API_KEY`` environment variables.
Only a tiny subset of the API is implemented so that the script can act
as a smoke test during development.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests

UPLOAD_URL = "https://api.vectara.io/v1/upload"


def _env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise EnvironmentError(f"Missing environment variable: {name}")
    return val


def upload_json(path: str) -> Dict[str, Any]:
    """Upload the documents contained in *path* to Vectara and return the JSON response."""

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = {
        "customerId": _env("VECTARA_CUSTOMER_ID"),
        "corpusId": _env("VECTARA_CORPUS_ID"),
        "document": data if isinstance(data, list) else [data],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": _env("VECTARA_API_KEY"),
    }

    resp = requests.post(UPLOAD_URL, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv

    load_dotenv()
    import sys

    print(upload_json(sys.argv[1]))
