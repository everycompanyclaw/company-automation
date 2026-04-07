# Weekly Metrics Report

**Category:** Reporting | **Apps:** Google Analytics + Stripe + HubSpot + Gmail | **Zap Steps:** 5

## What It Does

Compiles weekly metrics from Google Analytics, Stripe, and HubSpot, then sends a formatted digest email every Monday morning.

## Setup Instructions

### Step 1: Schedule — Every Monday 8:00 AM
- Use Zapier's "Schedule by Zapier" app
- Set to Weekly, Monday, 8:00 AM (your timezone)

### Step 2: Google Analytics — Get Metrics
- Connect GA4 property
- Metrics: sessions, users, newUsers, bounceRate, pageViews
- Date range: last 7 days

### Step 3: Stripe — Get Recent Charges
- Connect Stripe account
- List charges from last 7 days
- Calculate total revenue

### Step 4: HubSpot — Get New Contacts
- Connect HubSpot
- Filter: contacts created in last 7 days
- Count total new leads

### Step 5: Gmail — Send Report
- Connect Gmail account
- To: your team email
- Subject: "📊 Weekly Metrics Report — [Date Range]"
- Body: formatted digest with all metrics

## Customization

- Add Google Search Console metrics
- Add CRM deal pipeline changes
- Add social media follower counts
- Send to multiple recipients
- Add a Google Sheet row for historical tracking

## Notes

- GA4 requires an API connection setup in Google Cloud Console
- Consider using Data Studio for more complex reporting
- Adjust time based on when you want the report
