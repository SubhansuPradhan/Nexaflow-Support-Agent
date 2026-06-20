# Troubleshooting Guide

## Common Issues and Resolutions

### 1. Cannot Connect to the NexaFlow Dashboard

**Symptoms**: Page not loading, ERR_CONNECTION_REFUSED, blank white screen

**Steps**:
1. Check the NexaFlow status page at https://status.nexaflow.io
2. Test your internet connection by visiting another website
3. Disable browser extensions (especially ad blockers or VPNs) and retry
4. Clear browser cache: Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
5. Try an incognito/private window
6. Switch to a different browser
7. If using a corporate network, check if nexaflow.io is whitelisted by your IT team

**Root Cause**: Usually a DNS caching issue or a browser extension conflict. Cache clearing resolves 80% of cases.

### 2. API Returning 500 Internal Server Error

**Symptoms**: HTTP 500 responses on valid API calls

**Steps**:
1. Check https://status.nexaflow.io for ongoing incidents
2. Review the response body for an error code (e.g., NF-5001)
3. Verify your request payload matches the API schema (see API docs)
4. Test the same request with curl to rule out SDK issues
5. Check if the issue is endpoint-specific or affects all calls
6. Note the `x-request-id` header value and include it when contacting support

**Root Cause**: 500 errors are server-side. If not related to a known incident, the `x-request-id` allows engineers to trace the exact failure.

### 3. Webhooks Not Being Received

**Symptoms**: Webhook events are fired (visible in Webhook Logs) but not received by your endpoint

**Steps**:
1. Verify your endpoint URL is publicly accessible (not localhost)
2. Confirm your server responds with HTTP 200 within 5 seconds
3. Check if your firewall blocks incoming requests from NexaFlow IP ranges: 52.21.0.0/16, 34.198.0.0/16
4. Inspect the Webhook Logs in Dashboard > Integrations > Webhooks for delivery status
5. Test with a webhook testing service like webhook.site
6. Check your server logs for incoming POST requests

### 4. Slow Dashboard Performance

**Symptoms**: Pages take more than 5 seconds to load, charts not rendering

**Steps**:
1. Check your internet speed (minimum 5 Mbps recommended)
2. Reduce the date range on dashboard reports — large ranges slow queries
3. Clear browser cache and local storage
4. Disable browser extensions one at a time to identify conflicts
5. Try from a different device to determine if hardware is the factor

### 5. Email Notifications Not Arriving

**Steps**:
1. Check spam and junk folders
2. Verify notification preferences in Settings > Notifications
3. Add noreply@nexaflow.io and no-reply@nexaflow.io to your contacts
4. Ask your IT admin if nexaflow.io email domain is blocked by your mail server
5. If using a custom domain email, verify SPF/DKIM records are not rejecting the emails

## Collecting Diagnostic Information for Support
When contacting support, always include:
- Your account email
- The exact error message or HTTP error code
- The `x-request-id` header from API responses
- Browser name and version
- Steps to reproduce the issue
- Screenshot or screen recording if applicable
