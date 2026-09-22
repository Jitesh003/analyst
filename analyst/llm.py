"""The one LLM call the whole project is built on.

The plumbing below is boilerplate. ask() is yours -- about 8 lines.
Run it with:  python -m analyst.llm
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def ask(prompt: str) -> str:
   
    client = genai.Client()
    result =client.models.generate_content(
        model=os.environ["GEMINI_MODEL"],
        contents=prompt,
    )
    print(f"Prompt tokens: {result.usage_metadata.prompt_token_count}, Candidates tokens: {result.usage_metadata.candidates_token_count}")
    return result.text



if __name__ == "__main__":
    print(ask("Reply with exactly: skeleton online"))
