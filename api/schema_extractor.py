import os
import json
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))


def get_schema():
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        fks = inspector.get_foreign_keys(table_name)
        pk = inspector.get_pk_constraint(table_name)
        schema[table_name] = {
            "columns": [{"name": c["name"], "type": str(c["type"])} for c in columns],
            "primary_key": pk.get("constrained_columns", []),
            "foreign_keys": [
                {
                    "column": fk["constrained_columns"],
                    "references": f"{fk['referred_table']}.{fk['referred_columns']}",
                }
                for fk in fks
            ],
        }
    return schema


def get_sample_values(table, column, limit=5):
    with engine.connect() as conn:
        result = conn.execute(
            text(f'SELECT DISTINCT "{column}" FROM "{table}" WHERE "{column}" IS NOT NULL LIMIT :limit'),
            {"limit": limit},
        )
        return [str(row[0]) for row in result]


def schema_to_prompt_text(schema, sample_values=None):
    lines = []
    for table, meta in schema.items():
        cols = ", ".join(f'{c["name"]} ({c["type"]})' for c in meta["columns"])
        lines.append(f"Table {table}: {cols}")
        if meta["primary_key"]:
            lines.append(f"  Primary key: {', '.join(meta['primary_key'])}")
        for fk in meta["foreign_keys"]:
            lines.append(f"  Foreign key: {fk['column']} -> {fk['references']}")
        if sample_values and table in sample_values:
            for col, vals in sample_values[table].items():
                lines.append(f"  Sample values for {col}: {vals}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(json.dumps(get_schema(), indent=2))
