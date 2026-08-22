# Text-to-SQL Interface with Guardrails and Hallucination Detection

See the full build guide for detailed explanations of every step.

## File structure
```
text-to-sql-project/
├── .env.example          # copy to .env and fill in your values
├── .gitignore
├── requirements.txt
├── docker-compose.yml    # optional — only needed if you don't already have Postgres
├── seed.sql              # sample e-commerce schema + data
├── frontend.py           # Streamlit UI (optional)
├── app/
│   ├── __init__.py
│   ├── schema_extractor.py   # Phase 2: reads DB schema into text
│   ├── prompt_builder.py     # Phase 2: builds the LLM system prompt
│   ├── llm_client.py         # Phase 3: calls Groq to generate SQL
│   ├── guardrails.py         # Phase 3: blocks destructive/unsafe SQL
│   ├── executor.py           # Phase 3: runs SQL safely, read-only
│   ├── validation.py         # Phase 4: hallucination detection + confidence score
│   └── main.py               # Phase 5: FastAPI app tying it all together
└── eval/
    ├── golden_queries.json   # Phase 7: your test question bank
    └── run_evals.py          # Phase 7: automated eval runner
```

## Quick start
1. `python3 -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in `GROQ_API_KEY` and `DATABASE_URL`
4. Create the `demo` database and load sample data:
   ```
   psql postgres -c "CREATE DATABASE demo;"
   psql -d demo -f seed.sql
   ```
5. Create the read-only DB user (see guardrails.py comments / build guide Phase 3.3)
6. `uvicorn app.main:app --reload` → open http://localhost:8000/docs
7. (Optional) in a second terminal: `streamlit run frontend.py`



## Git commands

```
git pull(pull latest code)
git checkout -b feature/taskA (new branch)
git checkout branch name(changing branch)
git add .
git commit -m "comments"
git push
git fetch -p (to refresh branch list)
```