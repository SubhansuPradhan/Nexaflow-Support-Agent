# Data Security and Privacy Policy

## Data Storage and Encryption
- All data is encrypted at rest using AES-256
- Data in transit is protected using TLS 1.3
- Database backups are encrypted and stored in geographically separate regions
- Encryption keys are managed via AWS KMS with automatic annual rotation

## Data Residency
- Default: Data stored in US East (N. Virginia, us-east-1)
- EU customers: Request EU data residency (Frankfurt, eu-central-1) for GDPR compliance
- Enterprise customers can specify preferred region during onboarding

## Access Controls
- Role-based access control (RBAC) enforced at API and database level
- Employee access to customer data requires two-person approval
- All internal access is logged and audited quarterly
- Production database access requires VPN + hardware MFA

## Compliance Certifications
- SOC 2 Type II (renewed annually)
- ISO 27001 certified
- GDPR compliant (EU customers)
- CCPA compliant (California customers)
- HIPAA Business Associate Agreement available for Enterprise plans

## Incident Response
In the event of a security breach:
1. Affected customers are notified within 72 hours (GDPR requirement)
2. Incident report published on status.nexaflow.io
3. Root cause analysis provided within 14 days
4. Report suspected security incidents to security@nexaflow.io

## Data Retention
- Active account data: Retained for the duration of the subscription
- Deleted account data: Purged within 30 days of account deletion
- Backup data: Retained for 90 days
- Audit logs: Retained for 2 years

## Your Data Rights
- **Export**: Download all your data via Settings > Data Export
- **Deletion**: Submit a deletion request to privacy@nexaflow.io
- **Correction**: Update your data through the account settings
- **Portability**: Data exported in JSON or CSV format on request

## Third-Party Sub-processors
NexaFlow uses the following third-party services:
- AWS (infrastructure and storage)
- Stripe (payment processing)
- SendGrid (transactional email)
- PagerDuty (incident alerting)

A full list of sub-processors is available at https://nexaflow.io/legal/sub-processors
