import os
import time
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
readonly_engine = create_engine(os.getenv("READONLY_DATABASE_URL"))


def execute_safe(sql: str, row_limit=1000):
    start = time.time()
    with readonly_engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(text(sql))
            rows = result.fetchmany(row_limit)
            columns = list(result.keys())
            df = pd.DataFrame(rows, columns=columns)
        finally:
            trans.rollback()  # belt and suspenders even though the DB user is SELECT-only
    elapsed = time.time() - start
    return {
        "results": df.to_dict(orient="records"),
        "row_count": len(df),
        "execution_time_sec": round(elapsed, 3),
    }
