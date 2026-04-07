# Stripe to Dashboard

**Category:** Reporting | **Apps:** Stripe + Google Sheets | **Zap Steps:** 4

## What It Does

Syncs new Stripe payments and refunds to a Google Sheets spreadsheet for real-time revenue tracking and reporting.

## Setup Instructions

### Step 1: Trigger — New Stripe Payment
- Connect your Stripe account
- Event: "New Payment"
- Filter: `status = succeeded`

### Step 2: Action — Create Google Sheets Row
- Connect your Google Sheets account
- Spreadsheet: `[YOUR_REVENUE_TRACKER]`
- Sheet: `Payments`
- Columns: Timestamp, Customer Email, Amount, Currency, Invoice ID, Payment ID

### Step 3: Lookup (Optional)
- Use Google Sheets "Lookup Spreadsheet Row" to check for existing customer

### Step 4: Update Customer Sheet (Optional)
- If customer exists, update their total spend column

## Customization

- Add a filter for specific products/amounts
- Split by product line using line items
- Add a monthly summary sheet
- Connect to Google Data Studio for live charts

## Notes

- Stripe test mode works with this template
- Amount in Stripe is in cents (convert to dollars in formatter)
- Set up a separate Zap for "Refunds" events
