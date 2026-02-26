import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./financial_analysis.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(String, primary_key=True, index=True) 
    filename = Column(String)
    query = Column(String)
    status = Column(String, default="processing")
    result_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)