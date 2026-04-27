from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta
import urllib.parse
import re

def test_booking():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        hotel_name = "Caravelle Saigon"
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        next_day = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        
        url = f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel_name)}&checkin={tomorrow}&checkout={next_day}&group_adults=2&no_rooms=1&group_children=0"
        print("Visiting:", url)
        
        page.goto(url, wait_until="domcontentloaded")
        
        # Take a screenshot to see what booking gives us
        page.screenshot(path="booking_test.png")
        
        # Try to find price
        try:
            # Booking often uses data-testid="price-and-discounted-price"
            locator = page.locator('[data-testid="price-and-discounted-price"]').first
            locator.wait_for(timeout=5000)
            text = locator.inner_text()
            print("Found Booking price text:", text)
            
            # Extract numbers
            numbers = re.findall(r'\d+', text.replace(',', '').replace('.', ''))
            if numbers:
                price = int(numbers[0])
                print("Extracted price:", price)
        except Exception as e:
            print("Could not find Booking price:", e)
            print("Page title:", page.title())
            
        browser.close()

if __name__ == "__main__":
    test_booking()
