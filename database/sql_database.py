from pathlib import Path
from langchain_community.utilities import SQLDatabase

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "company.db"

db = SQLDatabase.from_uri(
    f"sqlite:///{DB_PATH}"
)