import sqlite3
import os
from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def initialize_database():
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    with open(SCHEMA_PATH, "r") as f:
        schema_script = f.read()

    conn = sqlite3.connect(settings.DB_PATH)
    try:
        conn.executescript(schema_script)
        conn.commit()
        logger.info(f"Database initialized successfully at {settings.DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
