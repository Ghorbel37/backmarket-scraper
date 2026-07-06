from playwright.sync_api import sync_playwright
# --- NEW V2.0 IMPORT ---
from playwright_stealth import Stealth 
import os

def fetch_pixel_8_pro_prices():
    url = "https://www.backmarket.fr/fr-fr/p/google-pixel-8-pro"
    
    # Create a directory to store cookies and session data
    user_data_dir = os.path.join(os.getcwd(), "browser_session")
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )
        
        # --- NEW V2.0 STEALTH APPLICATION ---
        # We now apply stealth to the whole context before getting the page
        Stealth().apply_stealth_sync(context)
        
        page = context.pages[0] if context.pages else context.new_page()
        
        print(f"Navigating to {url}...")
        
        try:
            page.goto(url, wait_until="domcontentloaded")
            
            page.wait_for_timeout(5000) 
            
            print("Cleaning up unwanted DOM elements...")
            page.evaluate("""
                () => {
                    const selectors = [
                        // --- 1. Popups & Hidden Containers ---
                        'div[class*="bg-surface-default-mid"]',
                        'div[class*="bg-surface-default-hi"]',
                        'div[aria-live="polite"]',
                        
                        // --- 2. Promotional Banners ---
                        'div[aria-label*="réduction immédiate"]',
                        'div[aria-label="Encore moins cher avec la revente"]',
                        
                        // --- 3. Empty/Spacing Flex Containers ---
                        'div[class="md:flex md:justify-center md:items-stretch mb-56"]',
                        'div[class="flex justify-center"]',
                        
                        // --- 4. Header & Footer (Broad Catch) ---
                        'header',                  // Standard HTML5 Header tag
                        'footer',                  // Standard HTML5 Footer tag
                        '[data-test*="header"]',   // Catch custom components with header data-test
                        '[data-test*="footer"]'    // Catch custom components with footer data-test
                    ];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => el.remove());
                    });
                }
            """)
            page.wait_for_timeout(5000) 

            html_content = page.content()
            if "DataDome" in html_content or "captcha" in html_content.lower():
                print("⚠️ CAPTCHA detected. Please solve it manually in the browser window.")
                print("The script is paused for 60 seconds. Once solved, the session will be saved.")
                page.wait_for_timeout(60000)
                html_content = page.content()
            
            price_elements = page.locator('text=/\\d+,\\d{2}\\s*€/').all_inner_texts()
            
            if price_elements:
                prices = list(set([price.strip() for price in price_elements]))
                print("\n📱 Pixel 8 Pro Prices found:")
                for price in sorted(prices):
                    print(f"- {price}")
            else:
                print("⚠️ Page loaded, but couldn't find price elements.")

        except Exception as e:
            print(f"An error occurred: {e}")
            
        finally:
            context.close()

if __name__ == "__main__":
    fetch_pixel_8_pro_prices()