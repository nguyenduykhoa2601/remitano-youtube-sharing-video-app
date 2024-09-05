from shared.status_code.schemas import StatusCodeSchema

STATUS_CODE = StatusCodeSchema(
    success_code=0,
    not_found_code=404,
    invalid_params=422,
    internal_server=500,
    auth_failed=401
)
