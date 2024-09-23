import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_repost_quote(prompt: str, tweet_content: str, number_of_quotes: int) -> list[str]:
    quotes = []
    user_prompt = prompt + " Tweet content: " + tweet_content
    for _ in range(number_of_quotes):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a meaningful repost quote with hashtags and an emoji"},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        quote = completion.choices[0].message.content.strip()
        quotes.append(quote)
    
    return quotes