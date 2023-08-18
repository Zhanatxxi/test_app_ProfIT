from fastapi import APIRouter

from currency.src.auth.api import api as auth_api
from currency.src.parser.main import parser_api
from currency.src.routes import tags
from currency.src.routes.tags import TAGS

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(auth_api, prefix='/auth', tags=TAGS[tags.AUTH])
api_v1.include_router(parser_api, prefix='/currency', tags=TAGS[tags.CURRENCY])
