import sys
import io
from playwright.sync_api import sync_playwright

# Set stdout encoding to utf-8 to handle special characters (like smart quotes) on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def scrape_quotes():
    # 1. Launches a browser using Playwright.
    # We use sync_playwright() as a context manager to handle the setup and teardown.
    with sync_playwright() as p:
        # Launching Chromium browser. 
        # headless=True means the browser will run in the background without a window.
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        
        # Creating a new page (equivalent to a new tab).
        page = browser.new_page()
        
        # 2. Navigates to https://quotes.toscrape.com/.
        print("Navigating to https://quotes.toscrape.com/...")
        page.goto("https://quotes.toscrape.com/")
        
        # 3. Extracts the text of the first 5 quotes on the page.
        # 4. Extracts the author of each of those quotes.
        # We use page.locator(".quote") to find all elements with the "quote" class.
        # Then we take the first 5 elements.
        print("Extracting quotes...\n")
        quotes = page.locator(".quote").all()
        
        # 5. Prints them to your terminal in a clean format.
        print("-" * 50)
        print(f"{'#':<3} | {'AUTHOR':<20} | {'QUOTE'}")
        print("-" * 50)
        
        count = 0
        for quote in quotes:
            if count >= 5:
                break
            
            # Extract text from the span with class "text"
            text = quote.locator(".text").inner_text()
            
            # Extract author from the small element with class "author"
            author = quote.locator(".author").inner_text()
            
            # Print in a clean format
            # We clean the quote text slightly if it's too long, but here we just print it.
            print(f"{count + 1:<3} | {author:<20} | {text}")
            count += 1
            
        print("-" * 50)
        
        # 6. Closes the browser.
        print("\nScraping complete. Closing browser.")
        browser.close()

if __name__ == "__main__":
    scrape_quotes()
