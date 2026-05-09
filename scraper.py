import json
import os
import random
import urllib.request
import urllib.parse
from datetime import datetime
import re
from playwright.sync_api import sync_playwright

PRICES_FILE = "prices.json"

HOTELS = [
    "CARAVELLE SAIGON",
    "REX HOTEL",
    "PARK HYATT SAIGON",
    "THE REVERIE SAIGON",
    "HOTEL MAJESTIC",
    "INTERCONTINENTAL",
    "SOFITEL SAIGON",
    "PULLMAN SAIGON",
    "NEW WORLD HOTEL",
    "LOTTE HOTEL SAIGON",
    "GRAND HOTEL SAIGON",
    "THE MYST DONG KHOI",
    "LIBERTY CENTRAL",
    "SILVERLAND YEN",
    "FUSION ORIGINAL",
    "HOTEL DES ARTS",
    "MAI HOUSE SAIGON",
    "RENAISSANCE RIVERSDE",
    "SHERATON SAIGON",
    "LE MERIDIEN SAIGON"
]

SERVICED_APARTMENTS = [
    "SOMERSET CHANCELLOR",
    "SOMERSET HCMC",
    "ASCOTT WATERFRONT",
    "OAKWOOD RESIDENCE",
    "SEDONA SUITES",
    "SHERWOOD RESIDENCE",
    "SILA URBAN LIVING",
    "INTERCON RESIDENCES",
    "CAPRI BY FRASER",
    "SAIGON DOMAINE"
]

def fetch_real_price(hotel_name, page=None):
    """
    Attempt to fetch real price from Google Travel Search using Playwright.
    Converts VND to USD if successful. Returns None if it fails.
    """
    if not page:
        print(f"[{hotel_name}] No Playwright page provided, skipping real fetch.")
        return None
        
    try:
        query = f"{hotel_name} HCMC"
        url = f"https://www.google.com/travel/search?q={urllib.parse.quote(query)}"
        print(f"  -> Scraping: {hotel_name} ...", end=" ")
        
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        # Wait a brief moment to allow prices to render
        page.wait_for_timeout(3500)
        
        # Try to extract prices matching VND or USD format
        price_texts = page.locator('span[aria-label*="price"], span:has-text("VND"), span:has-text("₫"), span:has-text("$")').all_inner_texts()
        
        for text in price_texts:
            # Check VND first
            matches_vnd = re.findall(r'₫([\d,\.]+)', text)
            if matches_vnd:
                # Find the first valid price
                for m in matches_vnd:
                    clean_str = m.replace(',', '').replace('.', '')
                    if clean_str.isdigit():
                        vnd_price = int(clean_str)
                        if vnd_price > 100000:  # sanity check (more than 100k VND)
                            usd_price = int(round(vnd_price / 25450))
                            print(f"Success! (${usd_price})")
                            return usd_price
                            
            # Check USD if no VND match found
            matches_usd = re.findall(r'\$([\d,\.]+)', text)
            if matches_usd:
                for m in matches_usd:
                    clean_str = m.replace(',', '').replace('.', '')
                    if clean_str.isdigit():
                        usd_price = int(clean_str)
                        if usd_price > 20:  # sanity check (more than $20)
                            print(f"Success! (${usd_price} directly)")
                            return usd_price
                            
        print("No valid price found.")
        return None
    except Exception as e:
        print(f"Failed. ({str(e).splitlines()[0]})")
        return None

def update_prices():
    # Load previous data to compare
    prev_data = {}
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r") as f:
            try:
                dataList = json.load(f)
                if isinstance(dataList, list):
                    for item in dataList:
                        prev_data[item["name"]] = item["price"]
            except:
                pass
                
    # Load history for 7-day average
    HISTORY_FILE = "history.json"
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                pass
                
    today_str = datetime.now().strftime('%Y-%m-%d')
    hist_past = [entry for entry in history if entry.get("date") != today_str]
    hist_past.sort(key=lambda x: x["date"])
    # We need 14 days of history
    last_14_days = hist_past[-14:]
    
    # Split into prev 7 days and recent 7 days
    if len(last_14_days) > 7:
        prev_7_days = last_14_days[:-7]
        recent_7_days = last_14_days[-7:]
    else:
        # Not enough history for a true comparison, just use what we have
        prev_7_days = []
        recent_7_days = last_14_days
        
    last_30_days = hist_past[-30:] if len(hist_past) > 0 else []
        
    def get_averages(day_list):
        avg_dict = {}
        if not day_list: return avg_dict
        counts = {}
        for entry in day_list:
            for prop in entry["data"]:
                name = prop["name"]
                avg_dict[name] = avg_dict.get(name, 0) + prop["price"]
                counts[name] = counts.get(name, 0) + 1
        for name in avg_dict:
            avg_dict[name] /= counts[name]
        return avg_dict
        
    avg_prev = get_averages(prev_7_days)
    avg_recent = get_averages(recent_7_days)
    avg_30d = get_averages(last_30_days)
                
    new_data = []
    
    # Base starting prices if no history (Price per night for standard double)
    base_prices = {
        "CARAVELLE SAIGON": 150,
        "REX HOTEL": 110,
        "PARK HYATT SAIGON": 280,
        "THE REVERIE SAIGON": 320,
        "HOTEL MAJESTIC": 130,
        "INTERCONTINENTAL": 180,
        "SOFITEL SAIGON": 160,
        "PULLMAN SAIGON": 140,
        "NEW WORLD HOTEL": 135,
        "LOTTE HOTEL SAIGON": 145,
        "GRAND HOTEL SAIGON": 120,
        "THE MYST DONG KHOI": 155,
        "LIBERTY CENTRAL": 90,
        "SILVERLAND YEN": 85,
        "FUSION ORIGINAL": 170,
        "HOTEL DES ARTS": 190,
        "MAI HOUSE SAIGON": 165,
        "RENAISSANCE RIVERSDE": 150,
        "SHERATON SAIGON": 175,
        "LE MERIDIEN SAIGON": 185,
        "SOMERSET CHANCELLOR": 120,
        "SOMERSET HCMC": 110,
        "ASCOTT WATERFRONT": 200,
        "OAKWOOD RESIDENCE": 150,
        "SEDONA SUITES": 180,
        "SHERWOOD RESIDENCE": 140,
        "SILA URBAN LIVING": 130,
        "INTERCON RESIDENCES": 190,
        "CAPRI BY FRASER": 90,
        "SAIGON DOMAINE": 160
    }
    
    with sync_playwright() as p:
        print("Launching headless browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()

        for item in HOTELS + SERVICED_APARTMENTS:
            item_type = "hotel" if item in HOTELS else "apartment"
            real_price = fetch_real_price(item, page=page)
            
            is_stale = False
            # Determine current price
            if real_price is not None:
                current_price = real_price
            else:
                # Fallback to EXACT previous price and mark as stale
                current_price = prev_data.get(item, base_prices.get(item, 150))
                is_stale = True
                
            # Calculate trend
            old_price = prev_data.get(item, current_price)
            diff = current_price - old_price
            
            # Calculate Weekly Variance (Average of recent 7 days - Average of previous 7 days)
            avg_rec_price = avg_recent.get(item, current_price)
            avg_prv_price = avg_prev.get(item, avg_rec_price) 
            diff_7d = avg_rec_price - avg_prv_price
            
            trend = "FLAT"
            if diff > 0:
                trend = "UP"
            elif diff < 0:
                trend = "DOWN"
                
            new_data.append({
                "name": item,
                "price": current_price,
                "trend": trend,
                "diff": diff,
                "diff_7d": round(diff_7d),
                "avg_30d": round(avg_30d.get(item, current_price)),
                "type": item_type,
                "is_stale": is_stale
            })
            
        browser.close()
        
    # Save new prices
    with open(PRICES_FILE, "w") as f:
        json.dump(new_data, f, indent=4)
        
    # Save to history.json
    HISTORY_FILE = "history.json"
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                pass
                
    today_str = datetime.now().strftime('%Y-%m-%d')
    # Remove entry for today if it already exists to avoid duplicates
    history = [entry for entry in history if entry.get("date") != today_str]
    
    history.append({
        "date": today_str,
        "data": new_data
    })
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
        
    print("-----------------------------------------")
    print("Prices and history updated successfully.")
    print("-----------------------------------------")
    
    # Check if end of month
    import calendar
    import subprocess
    today = datetime.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]
    
    if today.day == 15 or today.day == last_day:
        print(f"[{today_str}] Report day (15th or end of month) detected. Generating & sending report...")
        try:
            subprocess.run(["python", "monthly_reporter.py"])
        except Exception as e:
            print("Failed to run monthly report:", e)

if __name__ == "__main__":
    print(f"Running daily price sync for HCMC Hotels & Apartments... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    update_prices()
