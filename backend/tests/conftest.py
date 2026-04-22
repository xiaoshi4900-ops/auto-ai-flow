import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        from app.seeds.seed_runner import seed_builtin_role_templates
        seed_builtin_role_templates(session)
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db.session import get_db_session

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db_session] = override_get_db

    original_hash = None
    original_verify = None
    try:
        from app.core import security
        original_hash = security.pwd_context.hash
        original_verify = security.pwd_context.verify
    except Exception:
        pass

    _password_store = {}

    def mock_hash(plain):
        return f"mock_hash_{plain}"

    def mock_verify(plain, hashed):
        return hashed == f"mock_hash_{plain}"

    with patch.object(security.pwd_context, "hash", side_effect=mock_hash), \
         patch.object(security.pwd_context, "verify", side_effect=mock_verify):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()
