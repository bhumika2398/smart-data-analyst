import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def load_file_to_sqlite(uploaded_file, db_path="data.db"):
    filename = uploaded_file.name
    table_name = os.path.splitext(filename)[0].lower().replace(" ", "_")

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    return engine, table_name


def get_table_info(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
        rows = result.fetchall()
        columns = list(result.keys())

    return {
        "table_name": table_name,
        "columns": columns,
        "sample_rows": [list(row) for row in rows]
    }


if __name__ == "__main__":
    import io

    test_path = "data/samples/test_sales.csv"

    with open(test_path, "rb") as f:
        content = f.read()

    file_obj = io.BytesIO(content)
    file_obj.name = "test_sales.csv"

    engine, table_name = load_file_to_sqlite(file_obj)
    info = get_table_info(engine, table_name)

    print("Table name:", info["table_name"])
    print("Columns:", info["columns"])
    print("Sample rows:")
    for row in info["sample_rows"]:
        print(" ", row)