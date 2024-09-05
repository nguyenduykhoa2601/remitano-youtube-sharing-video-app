from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from logging.log_database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    # Name of the service (e.g., "auth-middleware")
    service_name = Column(String, index=True)
    endpoint = Column(String, index=True)              # API endpoint called
    # HTTP method used (GET, POST, etc.)
    http_method = Column(String, index=True)
    # JSON string of request parameters
    request_params = Column(Text)
    # HTTP status code of the response
    response_status = Column(Integer)
    # JSON string of the response body
    response_body = Column(Text)
    # Error message if any occurred
    error_message = Column(Text, nullable=True)
    # Timestamp of the log
    timestamp = Column(DateTime, default=datetime.utcnow)
