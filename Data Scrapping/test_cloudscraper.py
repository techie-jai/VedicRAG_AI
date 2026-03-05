import cloudscraper
import time
from bs4 import BeautifulSoup

def test_with_cloudscraper():
    """Test fetching with cloudscraper to bypass Cloudflare"""
    print("=" * 60)
    print("Testing with cloudscraper (Cloudflare bypass)")
    print("=" * 60)
    
    try:
        # Create scraper instance
        scraper = cloudscraper.create_scraper()
        
        # Test 1: Index page
        print("\nTest 1: Fetching index page...")
        url = "https://www.sacred-texts.com/hin/index.htm"
        
        response = scraper.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        if response.status_code == 200:
            print("✓ Index page fetched successfully!")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            print(f"Found {len(links)} total links")
            
            # Find Hindu text links
            text_links = [link for link in links if '/hin/' in link.get('href', '')]
            print(f"Found {len(text_links)} Hindu text links")
            
            print("\nFirst 15 Hindu text links:")
            for i, link in enumerate(text_links[:15]):
                href = link.get('href')
                text = link.get_text().strip()
                print(f"  {i+1}. {href} -> {text[:50]}")
        else:
            print(f"✗ Failed with status {response.status_code}")
            return False
        
        # Test 2: Specific text
        print("\n" + "=" * 60)
        print("Test 2: Fetching specific text page")
        print("=" * 60)
        
        text_url = "https://www.sacred-texts.com/hin/upan/index.htm"
        print(f"\nFetching: {text_url}")
        
        response = scraper.get(text_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        if response.status_code == 200:
            print("✓ Text page fetched successfully!")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get page title
            title = soup.find('title')
            if title:
                print(f"Page title: {title.get_text()}")
            
            # Extract text content
            body = soup.find('body')
            if body:
                text = body.get_text()[:500]
                print(f"\nFirst 500 chars of content:\n{text}")
            
            # Find chapter/section links
            links = soup.find_all('a', href=True)
            print(f"\nFound {len(links)} links on page")
            
            # Show first few content links
            content_links = [link for link in links if link.get('href', '').endswith('.htm')]
            print(f"Found {len(content_links)} content links")
            print("\nFirst 10 content links:")
            for i, link in enumerate(content_links[:10]):
                href = link.get('href')
                text = link.get_text().strip()
                print(f"  {i+1}. {href} -> {text[:40]}")
            
            return True
        else:
            print(f"✗ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_texts():
    """Test fetching multiple text pages"""
    print("\n" + "=" * 60)
    print("Test 3: Fetching multiple text pages")
    print("=" * 60)
    
    urls = [
        ("Upanishads", "https://www.sacred-texts.com/hin/upan/index.htm"),
        ("Bhagavad Gita", "https://www.sacred-texts.com/hin/gita/index.htm"),
        ("Mahabharata", "https://www.sacred-texts.com/hin/maha/index.htm"),
        ("Ramayana", "https://www.sacred-texts.com/hin/rama/index.htm"),
    ]
    
    try:
        scraper = cloudscraper.create_scraper()
        
        for name, url in urls:
            print(f"\nFetching {name}...")
            response = scraper.get(url, timeout=10)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"  {status} Status: {response.status_code}, Content: {len(response.text)} bytes")
            time.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("\n🔍 TESTING SACRED-TEXTS.COM WITH CLOUDSCRAPER\n")
    
    success = test_with_cloudscraper()
    time.sleep(1)
    
    if success:
        test_multiple_texts()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)
