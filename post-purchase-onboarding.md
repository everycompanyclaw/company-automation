# Post-Purchase Email Onboarding Sequence
**EveryCompanyClaw | Created: 2026-04-14**

Trigger: Purchase confirmed via Stripe → Add customer to this sequence (Day 0, 3, 7, 14)

---

## Email 1 — Welcome & Download Instructions
**Send: Day 0 (immediately after purchase)**
**Subject:** Your EveryCompanyClaw tools are ready — here's how to get started 🚀

**Body:**

Hi {{first_name}},

Congratulations on your purchase — and welcome to EveryCompanyClaw.

You've just unlocked tools that will save you hours every week. Let's get you set up in the next 5 minutes.

**📬 Where to find your downloads:**

Check your email inbox (including spam) for a receipt from Stripe with your download links. If you don't see it within 10 minutes, email us at {{company_email}} and we'll send it directly.

**🔧 Quick setup for each product:**

**Python Scripts Bundle:**
```
1. Download the ZIP from your Stripe receipt
2. Install dependencies: pip install -r requirements.txt
3. Copy config.example.py → config.py and add your API keys
4. Run: python scripts/linkedin_scraper.py (or any script)
```

**Zapier Templates:**
```
1. Go to zapier.com and log in
2. Click "Create" → "From Template"
3. Search for the template name in our README
4. Connect your apps and activate
```

**AI Prompts Library:**
```
1. Open the prompts PDF or text file
2. Copy any prompt you need
3. Paste into ChatGPT, Claude, or Gemini
4. Done. No setup needed.
```

**💬 Need help?**

Open a GitHub issue at {{github_url}} or reply to this email. We typically respond within 4 hours.

— {{founder_name}}
EveryCompanyClaw

---

## Email 2 — Quick Win Guide (Day 3)
**Send: Day 3 after purchase**
**Subject:** 3 things you can automate this week with what you bought

**Body:**

Hi {{first_name}},

Hope you're getting value from your EveryCompanyClaw tools. I wanted to share the 3 most popular use cases from our community — things our most active users automate within their first week.

**⚡ Highest-impact automations for you:**

**1. Lead research on autopilot (Python Scripts)**
Run the LinkedIn scraper once and get a spreadsheet of prospect data. No more manual research.
```
python scripts/linkedin_scraper.py --query "fintech founders hong kong"
```

**2. New leads → Slack alert (Zapier Templates)**
Every time a form submission comes in, your team gets a Slack ping. No leads fall through the cracks.
Template: "New Lead → Slack Notification"

**3. First AI prompt (AI Prompts Library)**
Try the Cold Email Generator prompt — it's the #1 most-used prompt in the library.
Prompt: "Act as an expert copywriter. Write a cold email to [PROSPECT] that [BENEFIT]..."

**🎯 Your next step:**

Pick ONE of these three and run it this week. Just one. That's all it takes to start building the habit.

Reply to this email and tell me which one you tried — I read every response.

— {{founder_name}}
EveryCompanyClaw

---

## Email 3 — Cross-Sell: Complete Your Stack (Day 7)
**Send: Day 7 after purchase — only if customer bought a single product**
**Subject:** You have {{product_bought}}. Here's what's missing from your stack.

**Body:**

Hi {{first_name}},

You've been using {{product_bought}} for a week. How's it going?

I wanted to personally let you know about an offer we have running for founding members.

**You bought:** {{product_bought}}
**You're missing:** {{other_products}}

Together, all three tools cover your entire stack:
- **Python Scripts** → automates your backend data workflows
- **Zapier Templates** → connects all your apps without code
- **AI Prompts Library** → generates all your content in seconds

**Complete bundle pricing:**
You paid ${{price_paid}} for {{product_bought}}. The bundle is $99 total — so you'd add both remaining products for just ${{bundle_addon_price}} more.

→ {{stripe_bundle_link}}?utm_source=email&utm_medium=onboarding&utm_campaign=day7_crosssell&utm_content={{first_name}}

This is the same founding price you paid. No deadline, but once it's gone, it's gone.

— {{founder_name}}
EveryCompanyClaw

*P.S. Not interested? Totally fair — just reply and let me know. I won't follow up again unless you ask.*

---

## Email 4 — Review & Referral Request (Day 14)
**Send: Day 14 after purchase**
**Subject:** Did it deliver? + a favour to ask

**Body:**

Hi {{first_name}},

Two weeks in — I wanted to check in honestly.

**Did the tools deliver what you needed?**

I'm asking because your experience matters to us and to other founders who are deciding whether to try EveryCompanyClaw.

If you found it valuable, I'd really appreciate it if you could:
1. **Leave a Product Hunt review** (2 minutes): {{ph_product_url}}
2. **Refer a friend** — send them this link and you'll both get {{referral_bonus}}: {{referral_link}}

If it didn't meet expectations, I want to know why. Reply and tell me what went wrong — we offer full refunds within 30 days, no questions asked.

Either way, thank you for being a founding member.

— {{founder_name}}
EveryCompanyClaw

---

## Implementation Notes

### Trigger Setup (Stripe + Email)
- **Trigger:** Stripe payment_intent.succeeded webhook
- **Action:** Add customer email to email sequence tool (Resend, Mailchimp, ConvertKit, orBrevo/sendgrid)
- **Delay:** Send email N days after trigger (0, 3, 7, 14)
- **Personalization vars:** {{first_name}}, {{product_bought}}, {{price_paid}}, {{other_products}}, {{bundle_addon_price}}

### Product → Other Products Mapping
| Customer Bought | Missing Products |
|----------------|-----------------|
| Python Scripts Bundle | Zapier Templates + AI Prompts Library |
| Zapier Templates | Python Scripts + AI Prompts Library |
| AI Prompts Library | Python Scripts + Zapier Templates |
| Complete Bundle | None (no cross-sell email) |

### Bundle Add-On Price Calculator
| Original Purchase | Bundle Add-On Price |
|------------------|-------------------|
| Python Scripts ($79) | +$20 for Templates + Prompts |
| Zapier Templates ($49) | +$50 for Scripts + Prompts |
| AI Prompts ($29) | +$70 for Scripts + Templates |
| Complete Bundle | No cross-sell email sent |

### UTM Parameters for Attribution
```
utm_source=email
utm_medium=onboarding
utm_campaign=post_purchase_sequence
utm_content={{first_name}}
```

### Tools to Use
- **Resend** (recommended — already has API key in config)
- **ConvertKit** — great for product creators, easy tag-based sequences
- **Mailchimp** — free up to 500 subscribers, automation built-in
- **Brevo (Sendinblue)** — free up to 300 emails/day, good automation

### Email-Sending Agent Prompt
The Operations Agent should run this as a cron job:
- Check Stripe for new payments since last run
- For each new payment: send Email 1 immediately
- Tag customer with "onboarding_d1" in email tool
- Schedule Email 2 for Day 3, Email 3 for Day 7 (if single product), Email 4 for Day 14
- Track send dates in /tmp/company-automation/customer-onboarding-log.md

### Status Tracking
Track each customer through the sequence in `/tmp/company-automation/customer-onboarding-log.md`:
```
| customer_email | product | email1_sent | email2_sent | email3_sent | email4_sent | purchased_bundle |
```

---

*Last updated: 2026-04-14 | PM Agent*
