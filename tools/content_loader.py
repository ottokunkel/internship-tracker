import requests
from bs4 import BeautifulSoup
import re

def load_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the main content
        main_content = soup.get_text(separator='\n')

        # Clean up whitespace: remove extra spaces, newlines, and unwanted characters
        cleaned_content = re.sub(r'\s+', ' ', main_content)  # Collapse multiple spaces/newlines into one space
        cleaned_content = cleaned_content.strip()  # Remove leading and trailing spaces

        return cleaned_content
    else:
        raise Exception("Failed to load the webpage.")