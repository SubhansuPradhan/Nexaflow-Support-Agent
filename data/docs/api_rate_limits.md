# API Rate Limits

## Overview
NexaFlow enforces rate limits to ensure fair usage and platform stability. Rate limits are applied per API key.

## Rate Limit Tiers

| Plan       | Requests/minute | Requests/day | Burst limit |
|------------|-----------------|--------------|-------------|
| Free       | 10              | 1,000        | 20          |
| Starter    | 100             | 50,000       | 200         |
| Pro        | 500             | 500,000      | 1,000       |
| Enterprise | Custom          | Custom       | Custom      |

## Rate Limit Headers
Every API response includes these headers:
```
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1715000000
Retry-After: 12   (only present when rate-limited)
```

- `X-RateLimit-Limit`: Total requests allowed in the window
- `X-RateLimit-Remaining`: Requests remaining in the current window
- `X-RateLimit-Reset`: Unix timestamp when the window resets
- `Retry-After`: Seconds to wait before retrying (only on 429 responses)

## Handling 429 Too Many Requests
When you exceed the rate limit, NexaFlow returns HTTP 429 with:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Retry after 12 seconds.",
  "retry_after": 12
}
```

**Best practices for handling 429**:
1. Read the `Retry-After` header and wait that many seconds before retrying
2. Implement exponential backoff: wait 1s, then 2s, then 4s, up to a maximum of 60s
3. Use request queuing in high-volume scenarios
4. Cache responses where data does not change frequently

## Endpoint-Specific Limits
Some endpoints have stricter limits regardless of plan:
- `/auth/token`: 10 requests/minute (brute-force protection)
- `/users/invite`: 20 invitations/hour
- `/reports/export`: 5 exports/hour (large response payloads)

## Increasing Rate Limits
- **Starter/Pro**: Temporary limit increases available for approved use cases — contact support
- **Enterprise**: Custom limits negotiated as part of the contract

## Monitoring Usage
Track your API usage in Dashboard > API Gateway > Usage Analytics. Alerts can be configured to notify you when usage reaches 80% of your daily limit.
