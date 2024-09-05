from pydantic import BaseModel


class StatusCodeSchema(BaseModel):
    success_code: int
    not_found_code: int
    invalid_params: int
    internal_server: int
    auth_failed: int
