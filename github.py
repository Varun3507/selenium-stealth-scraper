import os
import time
import socket
import pandas as pd
import undetected_chromedriver as uc
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- WAIT FOR INTERNET ----------
def wait_for_internet(timeout=120):
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print(f"✅ Internet is back at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        except OSError:
            print(f"🔌 Internet down at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Retrying in 2 min...")
            time.sleep(timeout)

# ---------- SETUP STEALTH DRIVER ----------
def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    # headless=False for visibility; set True in production
    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/114.0.0.0 Safari/537.36"
    })
    return driver

# ---------- EXTRACT PROFILE DATA ----------
def extract_contractor_data(driver, link):
    wait_for_internet()
    driver.get(link)
    time.sleep(2)
    wait = WebDriverWait(driver, 10)

    def safe_select(css, attr=None):
        try:
            el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
            return el.get_attribute(attr).strip() if attr else el.text.strip()
        except:
            return ""

    name    = safe_select("h1.dockable.business-name")
    phone   = safe_select("a.phone.dockable span.full")
    website = safe_select("a.website-link.dockable", "href")
    address = safe_select("span.address")
    email_href = safe_select("a.email-business", "href")
    email   = email_href.replace("mailto:", "") if email_href.startswith("mailto:") else ""

    return {
        "Name": name,
        "Phone": phone,
        "Website": website,
        "Address": address,
        "Email": email,
        "Profile Link": link
    }

# ---------- SCRAPER FUNCTION ----------
def scrape_contractors_for_city(city_name, contractor_url, max_pages=100):
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    data = []

    safe_city_name = city_name.replace(" ", "_")
    filename = f"{safe_city_name}.csv"
    existing_links = set()

    if os.path.exists(filename):
        print(f"📄 Resuming from existing file: {filename}")
        existing_df = pd.read_csv(filename)
        existing_links = set(existing_df["Profile Link"].dropna().tolist())
        data.extend(existing_df.to_dict(orient="records"))

    try:
        for page in range(1, max_pages + 1):
            print(f"\n🌆 {city_name} — Processing page {page}...")
            url = f"https://www.your_website.com/{contractor_url}?page={page}" if page > 1 else f"https://www.your_website.com/{contractor_url}"
            wait_for_internet()
            driver.get(url)

            for attempt in range(3):
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.business-name")))
                    break
                except:
                    print(f"⚠ Retry {attempt+1}/3 — waiting for contractor links…")
                    time.sleep(2)
            else:
                print("❌ Could not load contractor links. Skipping city.")
                break

            links = [el.get_attribute("href")
                     for el in driver.find_elements(By.CSS_SELECTOR, "a.business-name")
                     if el.get_attribute("href")]

            for link in links:
                if link in existing_links:
                    print(f"⏭ Skipping already scraped: {link}")
                    continue

                print(f"🔎 Scraping: {link}")
                contractor_data = extract_contractor_data(driver, link)
                data.append(contractor_data)
                existing_links.add(link)

                # Optional: Save after each entry (safer but slower)
                pd.DataFrame(data).to_csv(filename, index=False)
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user! Saving collected data for this city…")

    finally:
        driver.quit()
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(df)} entries to '{filename}'")

# ---------- MAIN EXECUTION ----------
def main():
    cities_df = pd.read_csv("./new_updated_file_16to17.csv").iloc[26:]  # Modify this to pick more cities if needed
    for _, row in cities_df.iterrows():
        city_name = row["city"]
        contractor_url = row["contractor_url"]
        scrape_contractors_for_city(city_name, contractor_url, max_pages=100)

# ---------- RUN ----------
if __name__ == "__main__":
    main()