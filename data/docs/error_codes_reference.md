# Error Codes Reference

## HTTP Status Codes

### 4xx Client Errors

| Code | Meaning              | Common Cause                                     |
|------|----------------------|--------------------------------------------------|
| 400  | Bad Request          | Malformed JSON, missing required fields          |
| 401  | Unauthorized         | Missing, invalid, or expired authentication      |
| 403  | Forbidden            | Valid auth but insufficient permissions          |
| 404  | Not Found            | Resource does not exist or was deleted           |
| 409  | Conflict             | Duplicate resource or state conflict             |
| 422  | Unprocessable Entity | Validation failure on request body               |
| 429  | Too Many Requests    | Rate limit exceeded                              |

### 5xx Server Errors

| Code | Meaning               | Action                                           |
|------|-----------------------|--------------------------------------------------|
| 500  | Internal Server Error | Retry; contact support if persistent             |
| 502  | Bad Gateway           | Temporary — retry after 30 seconds               |
| 503  | Service Unavailable   | Check status.nexaflow.io; retry with backoff     |
| 504  | Gateway Timeout       | Request took too long; reduce payload or retry   |

## NexaFlow Application Error Codes

All application errors include a machine-readable code in the response body:

```json
{
  "error": "NF-1042",
  "message": "API key has been revoked.",
  "docs": "https://docs.nexaflow.io/errors/NF-1042"
}
```

### Authentication Errors (NF-10xx)
- **NF-1001**: Invalid API key format
- **NF-1002**: API key not found or deleted
- **NF-1003**: API key expired (keys expire after 365 days by default)
- **NF-1004**: OAuth token expired — use refresh token
- **NF-1005**: OAuth token revoked — re-authenticate user
- **NF-1042**: API key manually revoked by admin

### Permission Errors (NF-20xx)
- **NF-2001**: Insufficient scope — key does not have required permissions
- **NF-2002**: Account suspended — resolve billing issues
- **NF-2003**: Feature not available on current plan

### Validation Errors (NF-30xx)
- **NF-3001**: Required field missing
- **NF-3002**: Field value out of allowed range
- **NF-3003**: Invalid email format
- **NF-3004**: File size exceeds limit (max 50MB)

### Resource Errors (NF-40xx)
- **NF-4001**: Project not found
- **NF-4002**: User not found
- **NF-4003**: Webhook not found
- **NF-4004**: Integration not configured

### Server Errors (NF-50xx)
- **NF-5001**: Database timeout — temporary, retry
- **NF-5002**: Third-party service unavailable
- **NF-5003**: Internal processing error — include x-request-id when contacting support

## Debugging Tips
1. Always log the full response body, not just the status code
2. Record the `x-request-id` header — include it in all support tickets
3. Test endpoints with curl to isolate SDK vs API issues
4. Use the API explorer at https://docs.nexaflow.io/try for interactive testing
