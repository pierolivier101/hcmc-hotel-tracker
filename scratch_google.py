from playwright.sync_api import sync_playwright
import urllib.parse
import re

def test_google():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        hotel_name = "Park Hyatt Saigon"
        url = f"https://www.google.com/travel/search?q={urllib.parse.quote(hotel_name)}"
        print("Visiting:", url)
        
        page.goto(url, wait_until="domcontentloaded")
        page.screenshot(path="google_test.png")
        
        try:
            locator = page.locator('span[aria-label*="price"]').first
            locator.wait_for(timeout=10000)
            text = locator.inner_text()
            print("Found Google text:", text)
        except Exception as e:
            print("Could not find Google price:", e)
            print("Page title:", page.title())
            
        browser.close()

if __name__ == "__main__":
    test_google()
