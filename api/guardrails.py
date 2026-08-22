import re
import logging
import sqlparse

logging.basicConfig(filename="blocked_queries.log", level=logging.WARNING)

FORBIDDEN_KEYWORDS = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE", "GRANT", "REVOKE"]


class GuardrailViolation(Exception):
    pass


def validate_sql(sql: str, forbidden_keywords=None, max_subquery_depth=3, default_row_limit=1000):
    forbidden_keywords = forbidden_keywords or FORBIDDEN_KEYWORDS

    if not sql or not sql.strip():
        logging.warning("Blocked: empty SQL")
        raise GuardrailViolation("Empty SQL")

    parsed = sqlparse.parse(sql)
    if not parsed:
        logging.warning(f"Blocked: could not parse SQL -> {sql}")
        raise GuardrailViolation("Could not parse SQL")

    upper_sql = sql.upper()
    for word in forbidden_keywords:
        if re.search(rf"\b{word}\b", upper_sql):
            logging.warning(f"Blocked keyword '{word}' in query: {sql}")
            raise GuardrailViolation(f"Blocked keyword: {word}")

    if upper_sql.count("(SELECT") > max_subquery_depth:
        logging.warning(f"Blocked: too many nested subqueries -> {sql}")
        raise GuardrailViolation("Too many nested subqueries")

    if "LIMIT" not in upper_sql and "COUNT(" not in upper_sql and "SUM(" not in upper_sql and "GROUP BY" not in upper_sql:
        sql = sql.rstrip(";") + f" LIMIT {default_row_limit};"

    return sql
