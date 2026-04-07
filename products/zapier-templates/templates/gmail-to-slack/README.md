# Gmail to Slack Notifications

**Category:** Email Automation | **Apps:** Gmail + Slack | **Zap Steps:** 3

## What It Does

Monitors a Gmail inbox for emails matching specific criteria and forwards them to a designated Slack channel with a formatted summary.

## Setup Instructions

### Step 1: Trigger — New Email Matching Search
- Connect your Gmail account
- Search query: `from:(clients@ OR leads@) subject:(order OR inquiry OR quote)`
- Customize search based on your needs

### Step 2: Action — Format Email Summary
- Use Zapier Formatter:
  - Extract: Subject, From, Body (plain text, first 300 chars)
  - Create a summary string: "[From] Subject: [Subject]"

### Step 3: Action — Send Slack Message
- Connect your Slack account
- Channel: `#inbound-leads` or `#support-alerts`
- Message format: formatted summary with link to original email

## Customization

- Change the search query to match different priority levels
- Add a label in Gmail after forwarding
- Route to different Slack channels based on subject keywords
- Archive the email after sending to Slack

## Notes

- Use Gmail filters (not just Zapier search) to reduce API calls
- Never forward password reset or security emails to Slack
