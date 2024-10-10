from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate 
import tiktoken

# Schema for the details to be extracted from the job posting. 
json_schema = {
    "title": "jobs_post",
    "description": "Job Posting from a company.",
    "type": "object",
    "properties": {
        "Title": {
            "type": "string",
            "description": "Job Title that is posted in the listing",
        },
        "Company": {
            "type": "string",
            "description": "The company which is hiring",
        },
        "Location": {
            "type": "string",
            "description": "Location of the job, could be remote or in a specific location, or not listed at all.",
            "default": None,
        },
        "Description": {
            "type": "string",
            "description": "A very short summary of the job and what the company is looking for",
            "default": None,
        },
        "Experience": {
            "type": "integer",
            "description": "1-10 rating for what sort of experience level this job is for. 1 would be for intern. 10 would be for PhD",
            "default": None,
        },
        "Year_Desired": {
            "type": "integer",
            "description": "If listed, which earliest year of school this listing would prefer",
            "default": None,
        }

    },
    "required": ["Title", "Company", "Description", "Experience"],
}

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def extract_job_details(content, max_tokens: int):
    llm = ChatOpenAI(model="gpt-4o", max_tokens=500) 

    tokens_used = num_tokens_from_string(content, "cl100k_base")

    if (tokens_used >= max_tokens):
        return None

    print("tokens used: ", tokens_used)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value.",
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )
    runnable = prompt | llm.with_structured_output(schema=json_schema)

    output = runnable.invoke({"text": content})
    
    return output
 



