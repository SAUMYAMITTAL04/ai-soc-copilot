from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Create a local SQLite database file named 'soc_logs.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./soc_logs.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 2. Define the exact blueprint for our Enterprise Database Table
class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)
    raw_log = Column(String)
    analysis = Column(String)
    is_threat = Column(Boolean, default=False)

# 3. Actually build the table in the database
Base.metadata.create_all(bind=engine)