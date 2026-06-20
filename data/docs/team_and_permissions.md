# Team Management and Permissions Guide

## Roles and Permissions

| Permission                  | Viewer | Member | Admin | Owner |
|-----------------------------|--------|--------|-------|-------|
| View projects               | Yes    | Yes    | Yes   | Yes   |
| Create/edit tasks           | No     | Yes    | Yes   | Yes   |
| Create projects             | No     | Yes    | Yes   | Yes   |
| Delete projects             | No     | No     | Yes   | Yes   |
| Invite team members         | No     | No     | Yes   | Yes   |
| Manage billing              | No     | No     | No    | Yes   |
| Delete organization         | No     | No     | No    | Yes   |
| Access API Gateway          | No     | No     | Yes   | Yes   |
| Configure integrations      | No     | No     | Yes   | Yes   |

## Inviting Team Members
1. Go to Settings > Team > Invite Members
2. Enter the email address(es) — one per line, up to 20 at once
3. Select a role for the invitee
4. Click "Send Invitations"
5. Invitees receive an email valid for 7 days

If the recipient does not have a NexaFlow account, they will be prompted to create one during acceptance.

## Changing a Member's Role
1. Go to Settings > Team
2. Click the role dropdown next to the member's name
3. Select the new role
4. The change is immediate

Owners cannot change their own role. To downgrade yourself, first transfer ownership.

## Removing Team Members
1. Go to Settings > Team
2. Click "Remove" next to the member
3. Confirm the action
4. The member loses access immediately but their past contributions remain

## Guest Access
Enterprise plan customers can invite external guests (e.g., contractors or clients):
- Guests are limited to specific projects they are explicitly added to
- Guests have read-only access by default (configurable per project)
- Guests do not count toward the team member limit
- Guest access can be set to expire on a specific date

## Bulk Import Team Members
For organizations with many users:
1. Download the CSV template from Settings > Team > Bulk Import
2. Fill in email addresses and roles
3. Upload the CSV
4. Preview the list, then confirm

Limit: 200 members per bulk import.

## Team Activity Logs
Admins can view all team actions in Settings > Team > Activity Log:
- Login and logout events
- Permission changes
- Project creation and deletion
- API key management
- Logs are retained for 12 months (Enterprise: 24 months)
