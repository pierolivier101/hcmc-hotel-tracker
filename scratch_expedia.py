from playwright.sync_api import sync_playwright
import urllib.parse
import re

def test_expedia():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        hotel_name = "Park Hyatt Saigon"
        url = f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(hotel_name)}"
        print("Visiting:", url)
        
        page.goto(url, wait_until="domcontentloaded")
        page.screenshot(path="expedia_test.png")
        
        try:
            # Expedia price often has class contains "uitk-text" inside pricing section
            # Try to find a dollar sign
            locator = page.locator('div[data-test-id="price-summary"]').first
            locator.wait_for(timeout=10000)
            text = locator.inner_text()
            print("Found Expedia text:", text)
        except Exception as e:
            print("Could not find Expedia price:", e)
            print("Page title:", page.title())
            
        browser.close()

if __name__ == "__main__":
    test_expedia()
