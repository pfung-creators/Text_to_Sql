import json
from schema_extractor import get_schema, schema_to_prompt_text
from prompt_builder import build_prompt
from llm_client import generate_sql

question = "How many customers do we have?"

schema_text = schema_to_prompt_text(get_schema())
system_prompt, user_question = build_prompt(question, schema_text)
result = generate_sql(system_prompt, user_question)

print(json.dumps(result, indent=2))