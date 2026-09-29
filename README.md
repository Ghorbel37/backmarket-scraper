# Back Market Scraper

A Python script that opens a Back Market product page in a real browser and lists the prices it finds. It is set up for the Google Pixel 8 Pro on backmarket.fr.

## How it works

1. Opens the product page with Playwright in a visible Chromium window, with `playwright-stealth` applied so the page behaves like a normal visit.
2. Keeps cookies in a local `browser_session/` folder, so a solved CAPTCHA stays valid for later runs.
3. Removes pop-ups, banners, the header and the footer from the page.
4. If a CAPTCHA appears, waits 60 seconds so you can solve it in the browser window.
5. Collects every price in the `123,45 €` format and prints the unique values, sorted.

## Requirements

- Python 3.9+
- Chromium for Playwright

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python backmarket_scraper.py
```

Example output:

```
Navigating to https://www.backmarket.fr/fr-fr/p/google-pixel-8-pro...
Cleaning up unwanted DOM elements...

📱 Pixel 8 Pro Prices found:
- 389,00 €
- 412,00 €
```

To track another product, change the `url` in `fetch_pixel_8_pro_prices()`.

## Notes

- The browser runs with `headless=False` on purpose: Back Market's bot protection blocks most headless browsers.
- The page selectors match Back Market's layout at the time of writing and may need updating if the site changes.
