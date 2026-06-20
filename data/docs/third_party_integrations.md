# Third-Party Integrations Guide

## Available Integrations
NexaFlow integrates natively with 50+ tools across productivity, communication, and development categories.

### Communication
- **Slack**: Get task notifications and create tasks from Slack messages
- **Microsoft Teams**: Receive project updates in Teams channels
- **Email**: Create tasks by forwarding emails to your project inbox

### Development
- **GitHub**: Link pull requests to tasks; auto-close tasks on PR merge
- **GitLab**: Same as GitHub, for GitLab repositories
- **Jira**: Two-way sync between NexaFlow projects and Jira issues

### Cloud Storage
- **Google Drive**: Attach Drive files directly to tasks
- **Dropbox**: Link Dropbox folders to projects
- **OneDrive**: Access and attach OneDrive files within NexaFlow

### CRM
- **Salesforce**: Create support tasks from Salesforce cases
- **HubSpot**: Sync contact and deal information

## Connecting an Integration

### Slack Integration Setup
1. Go to Dashboard > Integrations > Slack
2. Click "Connect to Slack"
3. Select the Slack workspace and authorize
4. Choose a default channel for notifications
5. Configure which events trigger notifications (task created, due soon, completed, etc.)

### GitHub Integration Setup
1. Go to Dashboard > Integrations > GitHub
2. Click "Connect GitHub Account"
3. Authorize the NexaFlow GitHub App
4. Select repositories to connect
5. In NexaFlow tasks, use `#task-id` in commit messages to link them automatically

## Disconnecting an Integration
1. Go to Dashboard > Integrations
2. Click the connected integration
3. Click "Disconnect"
4. Confirm — existing linked data is preserved, but new sync stops

## Troubleshooting Integration Issues

### Slack Notifications Not Arriving
1. Verify the bot is in the target channel: type `/nexaflow status` in the channel
2. Check if the NexaFlow Slack app has been removed from the workspace
3. Re-authorize the Slack integration in Dashboard > Integrations > Slack > Reconnect

### GitHub Commits Not Linking
1. Ensure you are using the correct task ID format: `NF-123` or `#NF-123`
2. Verify the repository is connected in the integration settings
3. Check that the GitHub App has read access to the repository

## Zapier and Make.com
NexaFlow connects to 3,000+ apps via Zapier and Make.com:
- Zapier: https://zapier.com/apps/nexaflow
- Make.com: Search "NexaFlow" in Make.com's app directory

Use the NexaFlow API key for authentication in Zapier/Make.com.

## Custom Integrations via API
For tools not listed above, use the NexaFlow REST API or webhooks to build custom integrations. See the API Documentation and Webhook Setup Guide.
