import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# llama-3.3-70b-versatile is a good balance of quality/speed/cost for SQL generation.
# For an even cheaper/faster option on simple queries, try "llama-3.1-8b-instant".
MODEL = "llama-3.3-70b-versatile"


def generate_sql(system_prompt, user_question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)
