from fastapi import APIRouter

routerAuth = APIRouter(tags=['MW Auth'])

from routes.auth import *