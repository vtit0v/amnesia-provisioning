from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class AmneziaClient(Base):
    __tablename__ = "amnesia_clients"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(255), nullable=True)
    
    # Obfuscation parameters (random per client)
    h1 = Column(Integer)  # Random hash
    h2 = Column(Integer)  # Random hash
    h3 = Column(Integer)  # Random hash
    h4 = Column(Integer)  # Random hash
    
    # Config
    conf_content = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
