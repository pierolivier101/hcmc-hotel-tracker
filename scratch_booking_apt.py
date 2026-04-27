from playwright.sync_api import sync_playwright
import urllib.parse
import re
from datetime import datetime, timedelta

def test_booking_apt():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        name = "Somerset Chancellor Ho Chi Minh City"
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        next_day = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        
        url = f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(name)}&checkin={tomorrow}&checkout={next_day}"
        page.goto(url, wait_until="domcontentloaded")
        
        try:
            # We just need any element with data-testid="price-and-discounted-price"
            locator = page.locator('[data-testid="price-and-discounted-price"]').first
            locator.wait_for(timeout=10000)
            text = locator.text_content() # text_content() gets hidden text too, avoiding visibility timeouts
            print("Found Booking text:", text.encode('utf-8'))
        except Exception as e:
            print("Could not find price:", e)
            
        browser.close()

if __name__ == "__main__":
    test_booking_apt()
