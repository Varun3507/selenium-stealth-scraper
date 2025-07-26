# 🕵️‍♂️ YellowPages Stealth Scraper

A powerful, modular, and stealthy web scraper built using **Selenium**, **undetected-chromedriver**, and **Pandas** to extract contractor profile data from directory-style websites like YellowPages. Designed to bypass bot detection and resume progress safely after interruptions or network drops.

---

## ✨ Features

- 🔍 Extracts Name, Phone, Email, Website, and Address from business profile pages
- 📄 Resumable scraping — automatically skips already-scraped profiles
- 🧠 Smart waiting and retry logic for unstable pages
- 💻 Headless Chrome automation with anti-bot techniques
- 🌐 Automatically waits for internet before proceeding
- 🗂 Saves data city-wise in structured CSV files

---

## 🧱 How It Works

Here’s a step-by-step breakdown of how the scraper works, part by part. Each section of the code handles a specific task — from setting up the browser to navigating pages and extracting data — making the whole process smooth and reliable.

### 🔌 `wait_for_internet()`
Waits for internet availability before any network activity to avoid crashes during outages.

### 🕵️‍♀️ `setup_driver()`
Initializes a stealthy, headless Chrome browser using `undetected-chromedriver` with custom options to mimic human browsing and bypass detection.

### 🔍 `extract_contractor_data(driver, link)`
Extracts individual contractor profile details (Name, Phone, Website, Address, Email) from a given profile URL.

### 🌆 `scrape_contractors_for_city(city_name, contractor_url, max_pages)`
Loops through paginated business listings for a given city, opens each profile, extracts the data, and saves it to a CSV file. Skips previously scraped entries for efficiency.

### 🗃 `main()`
Reads a CSV of cities and their listing URLs and runs the scraper for each one.

---

## 🗂 Sample Input CSV (`new_updated_file_18to19.csv`)

| city       | contractor_url                          |
|------------|------------------------------------------|
| New York   | new-york-ny/general-contractors          |
| Los Angeles| los-angeles-ca/general-contractors       |

---

## 💾 Output

Each city gets its own CSV file (e.g., `New_York.csv`) with the following format:

```csv
Name,Phone,Website,Address,Email,Profile Link
"ABC Construction","(123) 456-7890","http://abc.com","123 Main St, NY","contact@abc.com",...
