import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.api import app, get_db

from fastapi.testclient import TestClient

# 1. In-memory SQLite engine
# 'check_same_thread=False' allows FastAPI async background threads to share the connection
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)

@pytest.fixture
def client(isolate_test_db_session):
    """Provides a FastAPI TestClient bound to the isolated in-memory DB session."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Build the database schema once at the start of the test run."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(autouse=True)
def isolate_test_db_session():
    """Wrap each individual test in an isolated, rolled-back transaction."""
    # Connect to the in-memory engine and begin a transaction block
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # Bind a SQLAlchemy session to this explicit connection
    db_session = TestingSessionLocal(bind=connection)

    # Tell FastAPI to use this isolated test session whenever a route calls get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Hand execution over to the test function
    yield db_session

    # TEARDOWN: Roll back every mutation made during the test and clear overrides
    db_session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()
