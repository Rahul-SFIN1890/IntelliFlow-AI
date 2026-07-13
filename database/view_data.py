import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/company.db"
)

query = "SELECT * FROM employees"

df = pd.read_sql_query(
    query,
    conn
)

print(df)

conn.close()