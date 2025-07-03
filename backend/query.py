"""Minimal Vectara search helper.

Provides ``search_vectara`` which performs a simple search against the
Vectara query API and returns the text of the top results.  Credentials
are read from environment variables:
``VECTARA_CUSTOMER_ID``, ``VECTARA_CORPUS_ID`` and ``VECTARA_API_KEY``.

This is meant as a lightweight smoke-test for the API.  Error handling
is intentionally sparse.
"""

from __future__ import annotations

import os
import requests
from typing import List


VECTARA_URL = "https://api.vectara.io/v1/query"


def _env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Missing environment variable: {name}")
    return value


def search_vectara(query: str, top_k: int = 3) -> List[str]:
    """Run a basic Vectara query and return the result texts."""

    data = {
        "query": [{"query": query, "start": 0, "top_k": top_k}],
        "customerId": _env("VECTARA_CUSTOMER_ID"),
        "corpusKey": [
            {"corpus_id": int(_env("VECTARA_CORPUS_ID")), "customer_id": int(_env("VECTARA_CUSTOMER_ID"))}
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": _env("VECTARA_API_KEY"),
    }

    resp = requests.post(VECTARA_URL, headers=headers, json=data, timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    responses = payload.get("responseSet", [{}])[0].get("response", [])
    return [r.get("text", "") for r in responses]


if __name__ == "__main__":
    # Example: print the top result for a sample query.
    from dotenv import load_dotenv

    load_dotenv()
    print(search_vectara("hello world", top_k=1))
