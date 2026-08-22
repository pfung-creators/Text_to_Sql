import re
from app.llm_client import client, MODEL


def back_translate(sql: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": f"What natural language question does this SQL query answer? Answer in one sentence.\n\nSQL:\n{sql}",
            }
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def compare_questions(original_question: str, back_translated: str) -> float:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "On a scale of 0 to 1, how well does question B match the intent of question A? "
                    f"Reply with ONLY a number like 0.8, nothing else.\n\nA: {original_question}\nB: {back_translated}"
                ),
            }
        ],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    try:
        return float(raw)
    except ValueError:
        match = re.search(r"[01](\.\d+)?", raw)
        return float(match.group()) if match else 0.5


def sanity_check(df):
    flags = []
    if df.empty:
        flags.append("Query returned zero rows — check if filters are too strict or wrong.")
    for col in df.columns:
        null_ratio = df[col].isna().mean() if len(df) else 0
        if null_ratio > 0.5:
            flags.append(f"Column '{col}' is more than 50% NULL — possible bad JOIN.")
    return flags


def compute_confidence(llm_confidence, alignment_score, sanity_flags, multi_query_agreement=None):
    score = 0.4 * llm_confidence + 0.4 * alignment_score
    score -= 0.1 * len(sanity_flags)
    if multi_query_agreement is not None:
        score = score * 0.7 + multi_query_agreement * 0.3
    return max(0.0, min(1.0, round(score, 2)))
