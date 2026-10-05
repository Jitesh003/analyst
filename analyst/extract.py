"""Stage 1: one 10-K filing -> typed JSON.

YOURS TO WRITE. The schema and the prompt are the whole exercise -- do not let
Claude Code write either one.

    extract(text: str) -> dict

Decide first, before any code:
  1. WHAT FIELDS? Pick 4-6. They must be (a) present in every 10-K, and
     (b) things you'd actually want to ask questions about later. Resist
     extracting everything -- a schema you can't verify by hand is useless
     at Stage 2.
  2. HOW DO YOU SAY "RETURN JSON"? You have two options. Pick one for today
     and know why:
       - ask for it in the prompt, parse the string yourself
       - config=types.GenerateContentConfig(response_mime_type="application/json")
     The first one breaks sometimes. That is the point. See the note below.
  3. WHAT GOES IN THE PROMPT besides the filing? Role, task, field
     definitions, what to do when a field is absent from the document.

SDK surface (same call as llm.py, one new argument):
    from google.genai import types
    client.models.generate_content(model=..., contents=..., config=...)
    types.GenerateContentConfig(response_mime_type=..., response_schema=...)

NOTE on today's choice: start WITHOUT the JSON mode. You want to see what
malformed output actually looks like, because Stage 1.3 is building the retry
that handles it. Turn the schema on afterwards and measure the difference --
that comparison is worth more than either answer alone.

One filing is ~88,000 tokens, so it fits in one call. No chunking yet.

Run it:  python -m analyst.extract ELF 2025
"""

from datetime import date
import json
import os
import sys

from google import genai
    
from analyst.corpus import load
from google.genai import types
from pydantic import BaseModel


class Filing(BaseModel):
    ceo_name: str
    company_name: str
    fiscal_year_end: date


def extract(text: str) -> dict:
    client = genai.Client()
    result =client.models.generate_content(
            model=os.environ["GEMINI_MODEL"],
            contents=f"need to extract ceo name company name and fiscal year end from the following text: {text}",
            config=types.GenerateContentConfig(response_mime_type="application/json",response_schema=Filing),
        )
    print(f"Prompt tokens: {result.usage_metadata.prompt_token_count}, Candidates tokens: {result.usage_metadata.candidates_token_count}")
    return result.parsed.model_dump(mode="json")


if __name__ == "__main__":
    ticker, year = sys.argv[1], int(sys.argv[2])
    filing = load(ticker, year)
    print(f"{ticker} {year}: {len(filing.split()):,} words in\n")
    print(json.dumps(extract(filing), indent=2))
