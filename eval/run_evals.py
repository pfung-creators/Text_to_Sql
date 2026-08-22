import json
import requests
import pandas as pd

API_URL = "http://localhost:8000"

with open("eval/golden_queries.json") as f:
    cases = json.load(f)

results = []
for case in cases:
    resp = requests.post(f"{API_URL}/v1/query", json={"question": case["question"]}).json()
    got_sql = resp.get("sql", "") or ""
    expected_sql = case.get("expected_sql") or ""
    exact_match = got_sql.strip().rstrip(";") == expected_sql.strip().rstrip(";")
    results.append(
        {
            "question": case["question"],
            "category": case["category"],
            "exact_match": exact_match,
            "confidence": resp.get("confidence"),
            "status": resp.get("status"),
        }
    )

df = pd.DataFrame(results)
print(df.groupby("category")["exact_match"].mean())
df.to_csv("eval/results.csv", index=False)
print("\nSaved detailed results to eval/results.csv")
