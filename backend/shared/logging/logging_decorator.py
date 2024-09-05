import functools
import logging
from shared.logging.log_services import log_to_db

logging.basicConfig(level=logging.INFO)


def log_api_call(service_name):
    """Decorator to log function calls with params, responses, and errors."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            endpoint = f"/{func.__name__}"    # Adjust as needed
            http_method = "POST"              # Adjust based on actual HTTP method

            logging.info(
                f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                response = await func(*args, **kwargs)
                log_to_db(service_name, endpoint, http_method, kwargs,
                          response.status_code, response.body, None)
                logging.info(f"Response from {func.__name__}: {response}")
                return response
            except Exception as e:
                log_to_db(service_name, endpoint, http_method,
                          kwargs, None, None, str(e))
                logging.error(f"Error in {func.__name__}: {e}")
                raise e

        return wrapper
    return decorator
