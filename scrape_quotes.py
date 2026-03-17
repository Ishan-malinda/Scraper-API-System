import sys
import io
import psycopg2
from playwright.sync_api import sync_playwright

# Set stdout encoding to utf-8 to handle special characters (like smart quotes) on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Supabase Pooled Connection (IPv4 compatible)
# REPLACE [YOUR-PASSWORD] with your actual database password
DATABASE_URL = "postgresql://postgres.bzumbpjeycetrmaammll:IMSsuperbasePass@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"

def save_to_db(author, text):
    """Helper function to insert a single record into Postgres"""
    conn = None
    try:
        # 1. Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 2. Create the table if it doesn't exist (Proactive step)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_quotes (
                id SERIAL PRIMARY KEY,
                author_name TEXT,
                extracted_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 3. The SQL command to insert data securely
        postgres_insert_query = """
            INSERT INTO scraped_quotes (author_name, extracted_text) 
            VALUES (%s, %s)
        """
        record_to_insert = (author, text)
        
        # 4. Execute and save (commit) the changes
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        print(f"Successfully saved to DB: {author}")
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into database:", error)
    finally:
        # 5. Always close the connection when done!
        if conn:
            cursor.close()
            conn.close()

def scrape_and_save():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Navigating to https://quotes.toscrape.com/...")
        page.goto("https://quotes.toscrape.com/")
        
        print("Extracting quotes...")
        quotes = page.locator(".quote").all()
        
        count = 0
        for quote in quotes:
            if count >= 5:
                break
            
            text = quote.locator(".text").inner_text()
            author = quote.locator(".author").inner_text()
            
            # Call our database function
            save_to_db(author, text)
            
            count += 1
            
        browser.close()
        print("\nScraping and Database Insertion Complete!")

if __name__ == "__main__":
    scrape_and_save()
