# Lead Capture to CRM

**Category:** Lead Management | **Apps:** Typeform + HubSpot | **Zap Steps:** 3

## What It Does

Captures new form submissions from Typeform and automatically creates a new contact in HubSpot CRM with all fields mapped correctly.

## Setup Instructions

### Step 1: Trigger — New Typeform Entry
- Connect your Typeform account
- Select form: `[YOUR_FORM_NAME]`
- Set "ID or entry ID" field

### Step 2: Action — Create HubSpot Contact
- Connect your HubSpot account
- Map fields:
  - `email` → Email
  - `name` → First Name
  - `name` → Last Name (split using formatter if needed)
  - `company` → Company Name
  - `phone` → Phone Number
  - `source` → Lead Source

### Step 3: Filter (Optional)
- Add a filter: "Email Address contains @" to skip invalid entries

## Customization

- Replace Typeform with Gravity Forms, JotForm, or Wufoo
- Replace HubSpot with Salesforce or Pipedrive
- Add a Slack notification step after contact creation
- Add contact to a specific HubSpot list based on form response

## Notes

- Make sure field names in your form match the HubSpot property names exactly
- Test with 3 sample submissions before turning on
