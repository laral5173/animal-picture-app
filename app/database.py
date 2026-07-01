"""
Database setup using SQLAlchemy + SQLite.
SQLite is embedded (no external server needed) - perfect for a
self-contained, portable build as required by the challenge.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./app/data/animals.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class AnimalPicture(Base):
    """A single saved animal picture record."""
    __tablename__ = "animal_pictures"

    id = Column(Integer, primary_key=True, index=True)
    animal_type = Column(String, index=True, nullable=False)  # cat, dog, bear
    source_url = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # where the image is stored locally
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    """Create tables and the data directory if they don't exist yet."""
    import os
    os.makedirs("./app/data", exist_ok=True)
    os.makedirs("./app/images", exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
