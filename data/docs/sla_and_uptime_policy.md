# Service Level Agreement (SLA) and Uptime Policy

## Uptime Commitments

| Plan       | Uptime SLA | Monthly Downtime Allowance |
|------------|------------|---------------------------|
| Free       | Best effort| No guarantee               |
| Starter    | 99.5%      | ~3.6 hours/month           |
| Pro        | 99.9%      | ~43.8 minutes/month        |
| Enterprise | 99.99%     | ~4.4 minutes/month         |

Uptime is measured on a rolling 30-day basis and excludes scheduled maintenance windows.

## What Counts as Downtime
Downtime is defined as any period when the NexaFlow API or dashboard is completely unavailable and not due to:
- Scheduled maintenance (communicated 48 hours in advance)
- Actions or omissions by the customer
- Force majeure events
- Third-party service failures outside NexaFlow's control

## Scheduled Maintenance
- Maintenance windows: Sundays 02:00–06:00 UTC
- All maintenance is announced on https://status.nexaflow.io at least 48 hours in advance
- Emergency maintenance may occur with less notice but will be communicated immediately

## SLA Credits

If NexaFlow fails to meet the committed uptime, customers are eligible for service credits:

| Uptime Achieved | Credit (% of monthly fee) |
|-----------------|---------------------------|
| 99.0% – 99.5%   | 10%                        |
| 95.0% – 99.0%   | 25%                        |
| Below 95.0%     | 50%                        |

Credits are applied to the next billing cycle. They do not carry cash value and cannot be refunded.

## How to Claim an SLA Credit
1. Submit a credit request to sla@nexaflow.io within 30 days of the incident
2. Include the incident date, duration, and impact description
3. NexaFlow will validate against monitoring logs within 10 business days
4. Approved credits are applied automatically to the next invoice

## Support Response Times

| Plan       | Priority | First Response | Resolution Target |
|------------|----------|---------------|------------------|
| Free       | Low      | 72 hours      | Best effort      |
| Starter    | Normal   | 24 hours      | 5 business days  |
| Pro        | High     | 4 hours       | 2 business days  |
| Enterprise | Critical | 1 hour        | 4 hours          |

## Incident Communication
- Real-time status: https://status.nexaflow.io
- Subscribe to status updates via email or RSS
- Enterprise customers receive direct Slack/Teams notifications for P1 incidents

## Escalation Path for Enterprise Customers
1. Submit ticket via support portal — tagged as P1/Critical
2. Dedicated Customer Success Manager notified within 15 minutes
3. Engineering on-call engaged within 30 minutes
4. Executive stakeholder update every 2 hours until resolution
