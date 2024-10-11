import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def load_website_content(url, min_content_length=70):
    # First attempt: Use requests to fetch the page content
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        cleaned_content = parse_and_clean_content(content)
        # Check if the content length is below the minimum threshold

        tokens = num_tokens_from_string(cleaned_content, "cl100k_base")

        if tokens <= min_content_length:
            print("Content is small; switching to Playwright.")
            content = load_with_playwright(url)
            cleaned_content = parse_and_clean_content(content)
        else:
            print("Content loaded with requests.")
            print("LOADING:", tokens)
    except requests.RequestException as e:
        print(f"Requests failed: {e}. Switching to Playwright.")
        content = load_with_playwright(url)
        cleaned_content = parse_and_clean_content(content)

    # Parse and clean the content
    return cleaned_content

def load_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the URL and wait until the network is idle
        page.goto(url, wait_until='networkidle', timeout=15000)

        # Optionally wait for additional time to ensure dynamic content is loaded
        page.wait_for_timeout(2000)  # Wait for 2 seconds

        # Get the page content
        content = page.content()

        # Close the browser
        browser.close()

    print("Content loaded with Playwright.")
    return content

def parse_and_clean_content(html_content):
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.get_text(separator='\n')

    # Clean up whitespace
    cleaned_content = re.sub(r'\s+', ' ', main_content)
    cleaned_content = cleaned_content.strip()

    return cleaned_content

