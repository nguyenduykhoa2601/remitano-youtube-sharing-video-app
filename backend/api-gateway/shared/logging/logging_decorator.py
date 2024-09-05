import functools
import logging
from fastapi import HTTPException
from shared.logging.log_services import log_to_db

logging.basicConfig(level=logging.INFO)


def log_api_call(service_name):
    """Decorator to log function calls with params, responses, and errors."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            endpoint = f"/{func.__name__}"  # Adjust if necessary

            logging.info(
                f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                response = await func(*args, **kwargs)

                # Log successful response
                log_to_db(service_name, endpoint, "UNKNOWN", kwargs,
                          response.status_code, response.body, None)
                logging.info(f"Response from {func.__name__}: {response}")
                return response
            except Exception as e:
                # Log the exception
                log_to_db(service_name, endpoint, "UNKNOWN",
                          kwargs, None, None, str(e))
                logging.error(f"Error in {func.__name__}: {e}")

                # Return an HTTP 500 Internal Server Error
                # Adjust this if using a different framework or response structure
                raise HTTPException(
                    status_code=500, detail="Internal Server Error")

        return wrapper
    return decorator
