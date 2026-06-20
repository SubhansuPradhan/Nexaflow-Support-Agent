# API Authentication Guide

## Overview
NexaFlow uses API keys and OAuth 2.0 for authentication. All API requests must include a valid authentication token in the request header.

## API Key Authentication

### Generating an API Key
1. Log in to your NexaFlow account
2. Navigate to Settings > API Gateway > API Keys
3. Click "Generate New Key"
4. Select the key scope: Read-Only, Read-Write, or Admin
5. Copy the key immediately — it will not be shown again

### Using API Keys in Requests
Include the key in the Authorization header:
```
Authorization: Bearer nexaflow_live_xxxxxxxxxxxxxxxxxxxxxxxx
```

Never include API keys in URLs or client-side code.

## OAuth 2.0 Authentication

### Supported Grant Types
- **Authorization Code** (recommended for web applications)
- **Client Credentials** (for server-to-server communication)
- **Refresh Token** (for long-lived sessions)

### Authorization Code Flow
1. Redirect the user to: `https://auth.nexaflow.io/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=read:projects write:projects`
2. Exchange the code for tokens: POST to `https://auth.nexaflow.io/oauth/token`
3. Include the access token in subsequent requests

### Token Expiry and Refresh
- Access tokens expire after 1 hour
- Refresh tokens expire after 30 days
- Use the refresh token to obtain a new access token without re-authentication:
```
POST https://auth.nexaflow.io/oauth/token
{
  "grant_type": "refresh_token",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

## Common Authentication Errors

### 401 Unauthorized
- The API key or token is missing, invalid, or expired
- Verify the Authorization header format: `Bearer <token>`
- Regenerate the API key if it was recently rotated

### 403 Forbidden
- The token is valid but does not have permission for the requested resource
- Check the key scope in Settings > API Gateway
- Ensure the user role has the required permissions

### 429 Too Many Requests
- Rate limit exceeded. See the Rate Limits documentation.
- Check the `Retry-After` header for the reset time

## API Key Security Best Practices
- Rotate API keys every 90 days
- Use environment variables to store keys, never hardcode them
- Use the minimum required scope for each key
- Monitor API key usage in the API Gateway dashboard
- Revoke unused keys immediately
