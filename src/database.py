from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define the SQLite database URL (creates a local file named 'atlas_ops.db')
DATABASE_URL = "sqlite:///./atlas_ops.db"

# 2. Create the SQLAlchemy engine (connects Python to the database file)
# check_same_thread=False is required specifically for SQLite in multi-threaded web servers like FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for our database models to inherit from
Base = declarative_base()

# 5. Dependency injection function for FastAPI to get a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
