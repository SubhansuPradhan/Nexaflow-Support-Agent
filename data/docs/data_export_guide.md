# Data Export Guide

## What You Can Export
NexaFlow allows you to export all of your data at any time, in multiple formats.

### Exportable Data
- Projects (name, description, settings, dates)
- Tasks (all fields, comments, attachments metadata)
- Team members (names, roles, join dates)
- API usage logs (last 90 days)
- Billing invoices (PDF format)
- Audit logs (Admin/Owner only)
- Webhook delivery logs

## Exporting Data

### Full Account Export
1. Go to Settings > Data Export
2. Click "Request Full Export"
3. Select the format: JSON (complete) or CSV (tabular data only)
4. Click "Generate Export"
5. You will receive an email with a download link within 30 minutes
6. The download link is valid for 48 hours

### Project-Level Export
1. Open a project
2. Click the three-dot menu (•••) > Export Project
3. Choose format: JSON, CSV, or Excel
4. The export downloads immediately for projects under 5,000 tasks

### Exporting Invoices
Go to Settings > Billing > Invoice History. Click "Download PDF" next to any invoice.

## Export Formats

### JSON Format
- Complete data export including all fields, metadata, and relationships
- Suitable for importing into other systems or archiving

### CSV Format
- Tabular format compatible with Excel and Google Sheets
- Separate files for projects, tasks, and members
- Attachment metadata included but not the attachment files themselves

## Attachment Export
Attachments are stored with external URLs (Google Drive, Dropbox, etc.). NexaFlow exports the links, not the files themselves. Download the actual files directly from the source storage service.

## Scheduled Exports (Enterprise)
Enterprise customers can configure automated exports:
1. Go to Settings > Data Export > Scheduled Exports
2. Set frequency (daily, weekly, monthly)
3. Choose destination: Email, S3 bucket, or SFTP server
4. Exports are encrypted in transit and at rest

## After Account Deletion
You can request a data export for up to 14 days after closing your account by emailing privacy@nexaflow.io. After 30 days, all data is permanently deleted and cannot be recovered.

## Import from Competitors
NexaFlow supports importing data from:
- Asana (via CSV export from Asana)
- Trello (via JSON export from Trello)
- Jira (via XML export from Jira)
- Monday.com (via Excel export)

To import, go to Dashboard > Import Data and follow the guided setup wizard.
