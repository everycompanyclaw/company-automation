#!/usr/bin/env python3
"""
Stripe Setup - Create products and payment links via API
"""
import os
import stripe
from stripe import api_key

# Get API key from environment or replace with your secret key
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_YOUR_KEY_HERE')

stripe.api_key = STRIPE_SECRET_KEY

PRODUCTS = [
    {"name": "Python Scripts Bundle", "price": 7900, "description": "20 automation scripts"},
    {"name": "Zapier Templates", "price": 4900, "description": "10 workflow templates"},
    {"name": "AI Prompts Library", "price": 2900, "description": "100+ AI prompts"},
]

def create_products():
    """Create products and payment links"""
    results = []
    
    for product in PRODUCTS:
        # Create product
        p = stripe.Product.create(
            name=product["name"],
            description=product["description"]
        )
        
        # Create price
        price = stripe.Price.create(
            product=p.id,
            unit_amount=product["price"],
            currency="usd"
        )
        
        # Create payment link
        link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            after_completion={"type": "redirect", "redirect": {"url": "https://everycompanyclaw.github.io/company-automation/"}}
        )
        
        results.append({
            "product": product["name"],
            "price_cents": product["price"],
            "payment_link": link.url
        })
        print(f"✅ {product['name']}: {link.url}")
    
    return results

def save_links(links):
    """Save payment links to file"""
    with open("/Users/macbookpro/.openclaw/workspace/company/automation/data/payment_links.json", "w") as f:
        import json
        json.dump(links, f, indent=2)

if __name__ == "__main__":
    print("🔗 Creating Stripe products and payment links...\n")
    results = create_products()
    save_links(results)
    print("\n✅ All products created! Links saved.")
