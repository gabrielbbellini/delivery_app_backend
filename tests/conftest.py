import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Base
from tests.database import engine_test, override_get_db

from src.database import get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # limpa e recria as tabelas para a sessão de testes
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client():
    # sobrescreve o get_db para usar banco SQLite
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client

    # limpa os overrides depois
    app.dependency_overrides.clear()
