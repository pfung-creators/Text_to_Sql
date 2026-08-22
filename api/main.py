import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from app.schema_extractor import get_schema, schema_to_prompt_text
from app.prompt_builder import build_prompt
from app.llm_client import generate_sql
from app.guardrails import validate_sql, GuardrailViolation
from app.executor import execute_safe
from app.validation import back_translate, compare_questions, sanity_check, compute_confidence

app = FastAPI(title="Text-to-SQL API")

history = []  # simple in-memory store to start; swap for a DB table later


class QueryRequest(BaseModel):
    question: str


@app.get("/v1/schema")
def schema():
    return get_schema()


@app.get("/v1/history")
def get_history():
    return history


@app.post("/v1/query")
def query(req: QueryRequest):
    schema_text = schema_to_prompt_text(get_schema())
    system_prompt, question = build_prompt(req.question, schema_text)
    llm_output = generate_sql(system_prompt, question)

    if llm_output.get("clarification_needed"):
        return {"status": "needs_clarification", "options": llm_output["clarification_needed"]}

    try:
        safe_sql = validate_sql(llm_output["sql"])
    except GuardrailViolation as e:
        return {"status": "blocked", "reason": str(e)}

    exec_result = execute_safe(safe_sql)
    back_q = back_translate(safe_sql)
    alignment = compare_questions(req.question, back_q)

    df = pd.DataFrame(exec_result["results"])
    flags = sanity_check(df)
    confidence = compute_confidence(llm_output.get("confidence", 0.5), alignment, flags)

    response = {
        "status": "ok",
        "question": req.question,
        "sql": safe_sql,
        "explanation": llm_output.get("explanation"),
        "results": exec_result["results"],
        "row_count": exec_result["row_count"],
        "execution_time_sec": exec_result["execution_time_sec"],
        "confidence": confidence,
        "warnings": flags,
    }
    history.append(response)
    return response
