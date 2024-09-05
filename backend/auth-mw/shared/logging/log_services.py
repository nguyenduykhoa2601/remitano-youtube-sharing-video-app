from sqlalchemy.orm import Session
from shared.logging.log_schemas import Log
from shared.logging.log_database import SessionLocal


def log_to_db(service_name, endpoint, http_method, request_params, response_status, response_body, error_message):
    """Log API call details into the database."""
    db: Session = SessionLocal()
    log = Log(
        service_name=service_name,
        endpoint=endpoint,
        http_method=http_method,
        request_params=request_params,
        response_status=response_status,
        response_body=response_body,
        error_message=error_message
    )
    db.add(log)
    db.commit()
    db.close()
