import os
import openai
import asyncio
from typing import List, Dict, Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    from openai.error import RateLimitError
except ImportError:
    try:
        from openai.errors import RateLimitError
    except ImportError:
        class RateLimitError(Exception):
            pass

async def call_llm(messages: List[Dict[str, str]], model: str = "gpt-4o") -> Optional[str]:
    max_retries = 5
    backoff = 1

    for attempt in range(max_retries):
        try:
            response = await asyncio.to_thread(
                openai.chat.completions.create,
                model=model,
                messages=messages
            )
            return response.choices[0].message.content

        except RateLimitError:
            print(f"Rate limit hit; retrying in {backoff}s (attempt {attempt+1}/{max_retries})")
            await asyncio.sleep(backoff)
            backoff *= 2

        except Exception as e:
            print(f"Unexpected LLM call error: {e}")
            await asyncio.sleep(backoff)
            backoff *= 2

    print(f"Failed to get LLM response after {max_retries} retries.")
    return None
