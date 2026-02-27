from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

# SQLite database stored in workspace
engine = create_engine('sqlite:///analysis.db', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(Text)
    file_path = Column(Text)
    result = Column(Text, nullable=True)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
