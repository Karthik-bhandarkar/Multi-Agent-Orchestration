import pytest
from src.db.init_db import initialize_database


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    initialize_database()
