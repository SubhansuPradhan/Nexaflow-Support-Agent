# Webhook Setup Guide

## Overview
Webhooks allow NexaFlow to push real-time event notifications to your server when specific actions occur, eliminating the need for polling.

## Supported Webhook Events
- `project.created` / `project.updated` / `project.deleted`
- `task.created` / `task.updated` / `task.completed`
- `user.invited` / `user.joined` / `user.removed`
- `api_key.created` / `api_key.revoked`
- `billing.payment_succeeded` / `billing.payment_failed`
- `integration.connected` / `integration.disconnected`

## Creating a Webhook
1. Go to Dashboard > Integrations > Webhooks
2. Click "Add Webhook"
3. Enter your endpoint URL (must be HTTPS)
4. Select events to subscribe to
5. Click "Create" — a test event will be sent immediately

## Webhook Payload Structure
```json
{
  "id": "wh_evt_01J2K8M3N4P5Q6R7",
  "event": "task.completed",
  "created_at": "2024-03-15T10:30:00Z",
  "data": {
    "task_id": "task_abc123",
    "project_id": "proj_xyz789",
    "completed_by": "user_def456",
    "completed_at": "2024-03-15T10:29:55Z"
  }
}
```

## Verifying Webhook Signatures
Every webhook includes an `X-NexaFlow-Signature` header. Verify this to confirm the request came from NexaFlow:

```python
import hmac
import hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

Your webhook secret is shown once at creation time. Store it securely.

## Retry Policy
NexaFlow retries failed webhook deliveries (non-200 responses or timeouts):
- Retry 1: 5 minutes after failure
- Retry 2: 30 minutes after failure
- Retry 3: 2 hours after failure
- Retry 4: 8 hours after failure
- After 4 failures, the webhook is marked as failed and delivery stops

Your endpoint must respond with HTTP 200 within 5 seconds.

## Viewing Webhook Logs
Dashboard > Integrations > Webhooks > [Select Webhook] > Delivery Logs shows:
- Timestamp of each delivery attempt
- HTTP response code
- Response body (first 1KB)
- Retry history

## Common Issues
- **Receiving duplicate events**: Implement idempotency using the `id` field
- **High latency in processing**: Accept the webhook immediately and process async
- **Signature verification failing**: Ensure you verify the raw request body, not a parsed/re-serialized version
