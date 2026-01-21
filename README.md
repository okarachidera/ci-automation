# B12 CI Submission

This repo contains a minimal Python script plus a GitHub Actions workflow that submits a signed JSON payload to the B12 challenge endpoint on every push.

## What it does

- Builds the required JSON payload with sorted keys and compact UTF-8 encoding.
- Signs the raw JSON bytes using HMAC-SHA256 and the required secret.
- POSTs to the submission endpoint and prints the receipt on success.

## GitHub Actions flow

The workflow runs on every push and:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Exports required environment variables and runs `submit.py`.

## Required secrets

Set these repository secrets in GitHub:

- `B12_NAME` — your full name
- `B12_EMAIL` — the email address you are applying with

The workflow provides `B12_REPOSITORY` and `B12_ACTION_RUN` directly from the GitHub context.

## Receipt

On success, the script prints:

```
RECEIPT: <receipt>
```

You can find this line in the GitHub Actions logs for the `Submit payload` step.
