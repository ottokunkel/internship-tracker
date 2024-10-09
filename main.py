from langchain import OpenAI, Document, WebPageLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Step 1: Set up your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Step 2: Define a function to load and parse the website content
def load_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the main content
        main_content = soup.get_text(separator='\n')
        return main_content
    else:
        raise Exception("Failed to load the webpage.")

# Step 3: Use Langchain to summarize the content
def summarize_content(content, max_tokens=200):
    openai_llm = OpenAI(temperature=0.5)
    prompt_template = PromptTemplate(
        input_variables=["content"],
        template="""
        Please provide a concise summary of the following content:
        "{content}"
        """
    )
    chain = LLMChain(llm=openai_llm, prompt=prompt_template)
    summary = chain.run(content=content, max_tokens=max_tokens)
    return summary

# Step 4: Create a function to export summaries to an Excel file
def export_summaries_to_excel(summaries, filename='webpage_summaries.xlsx'):
    df = pd.DataFrame(summaries, columns=["URL", "Summary"])
    df.to_excel(filename, index=False)
    print(f"Exported summaries to {filename}")

# Step 5: Main function to glue everything together
def main(urls):
    summaries = []
    for url in urls:
        print(f"Processing: {url}")
        try:
            content = load_website_content(url)
            summary = summarize_content(content)
            summaries.append((url, summary))
        except Exception as e:
            print(f"Failed to process {url}: {e}")
    
    # Export summaries to Excel
    export_summaries_to_excel(summaries)

if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://anotherwebsite.com"
    ]
    main(urls)