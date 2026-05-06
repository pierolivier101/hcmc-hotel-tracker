import json
from playwright.sync_api import sync_playwright

def test_google_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        url = "https://www.google.com/travel/search?q=SOMERSET%20D1&g2lb=4965990%2C72471280%2C72560029%2C72573224%2C72647020%2C72686036%2C72803964%2C72882230%2C72958624%2C73059275%2C73064764%2C121608705%2C121645061&hl=en-VN&gl=vn&ssta=1&ts=CAESCgoCCAMKAggDEAAaHBIaEhQKBwjqDxAFGBwSBwjqDxAFGB0YATICEAAqBwoFOgNWTkQ&qs=CAEyFENnc0ltX3J1enJDMl84bm9BUkFCOAhCCRGhoVtMOjSaOUIJEXtf7sCXrlHeQgkRWBbGASOD_y1qHAoaDbI9QEoSEwjBqvXa0p-UAxXqG3sHHZzLBwc&ap=aAG6AQhvdmVydmlldw&ictx=111&ved=0CAAQ5JsGahcKEwjA1o_l0p-UAxUAAAAAHQAAAAAQBQ"
        print("Visiting URL...")
        
        page.goto(url, wait_until="domcontentloaded")
        
        # Try to extract prices
        prices = page.locator('span[aria-label*="price"], span:has-text("VND")').all_inner_texts()
        
        with open("prices_output.json", "w", encoding="utf-8") as f:
            json.dump(prices, f, ensure_ascii=False, indent=4)
        
        browser.close()

if __name__ == "__main__":
    test_google_url()
