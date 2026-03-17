#!/usr/bin/env python3
"""Social Media Auto-Poster"""
import schedule
import time

def post():
    print("Posting to social media...")

schedule.every().day.at("09:00").do(post)

while True:
    schedule.run_pending()
    time.sleep(60)
