#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone

import requests


API_URL = "https://b12.io/apply/submission"
SECRET = b"hello-there-from-b12"
RESUME_LINK = "https://drive.google.com/file/d/180xAcfuYn9-zQzRn1lI4Nd8Dxmknx8Lz/view?usp=sharing"

ENV_NAME = "B12_NAME"
ENV_EMAIL = "B12_EMAIL"
ENV_REPOSITORY = "B12_REPOSITORY"
ENV_ACTION_RUN = "B12_ACTION_RUN"


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def build_payload() -> dict:
    return {
        "action_run_link": required_env(ENV_ACTION_RUN),
        "email": required_env(ENV_EMAIL),
        "name": required_env(ENV_NAME),
        "repository_link": required_env(ENV_REPOSITORY),
        "resume_link": RESUME_LINK,
        "timestamp": current_timestamp(),
    }


def main() -> int:
    try:
        payload = build_payload()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    raw_json = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    digest = hmac.new(SECRET, raw_json, hashlib.sha256).hexdigest()
    headers = {
        "X-Signature-256": f"sha256={digest}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, data=raw_json, headers=headers, timeout=30)
    except requests.RequestException as exc:
        print(f"REQUEST_ERROR: {exc}", file=sys.stderr)
        return 3

    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("ERROR: Response was not valid JSON", file=sys.stderr)
            return 4
        receipt = data.get("receipt")
        if receipt is None:
            print("ERROR: Missing receipt in response", file=sys.stderr)
            return 5
        print(f"RECEIPT: {receipt}")
        return 0

    print(f"{response.status_code} {response.text}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
