from typing import List, Union
import requests
import json
from pydantic import BaseModel


class Resume(BaseModel):
    name: str
    skills: List[str]

def create_prompt(input_text: str) -> str:
    PROMPT_TEMPLATE = f"""Parse the following resume and return a structured representation of the data in the schema below.
Resume:
---
{input_text}
---

Schema:
{Resume.model_json_schema()['properties']}

Output JSON:
"""
    return PROMPT_TEMPLATE

def extract_resume(input_text: str) -> Union[Resume, None]:
    prompt = create_prompt(input_text)
    
    # Call Ollama API
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral:latest",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        output = result.get("response", "")

        print(f"Output from Ollama API:\n{output}\n")

        if output:
            # Try to parse the JSON response
            try:
                json_data = json.loads(output)
                return Resume.model_validate(json_data)
            except json.JSONDecodeError:
                # If it's not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', output, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    json_data = json.loads(json_str)
                    return Resume.model_validate(json_data)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    # Example resume text
    resume_text = """
    John Doe
    Software Engineer with 5 years of experience
    
    Skills:
    - Python programming
    - Machine Learning
    - Web Development
    - Database Management
    - API Development
    
    Experience:
    - Senior Developer at Tech Corp (2020-2025)
    - Junior Developer at StartupXYZ (2019-2020)
    """
    
    print("Extracting resume information...")
    print(f"Input text:\n{resume_text}\n")
    
    result = extract_resume(resume_text)
    
    if result:
        print("Extracted resume:")
        print(f"Name: {result.name}")
        print(f"Skills: {result.skills}")
    else:
        print("Failed to extract resume information")

if __name__ == "__main__":
    main()
