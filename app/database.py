import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Look for a Cloud URL first, otherwise fall back to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./soc_logs.db")

# 2. Fix the URL prefix if necessary (SQLAlchemy requires 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Connect to the vault! (SQLite needs a special thread rule, Cloud Postgres does not)
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)
    raw_log = Column(String)
    analysis = Column(String)
    is_threat = Column(Boolean, default=False)

# Build the tables
Base.metadata.create_all(bind=engine)