from fastapi import APIRouter, Depends

from currency.src.auth.services import require_user
from currency.src.parser.schemas import ValueCurrencySchema, RangeCurrencySchema, ValueCurrencyRangeSchema
from currency.src.parser.services import parse_to_day, parse_to_range

parser_api = APIRouter()


@parser_api.get("/", response_model=list[ValueCurrencySchema])
async def get_currency(
        user_id: str = Depends(require_user)
):
    return await parse_to_day()


@parser_api.post("/", response_model=list[ValueCurrencyRangeSchema])
async def get_range(data: RangeCurrencySchema, user_id: str = Depends(require_user)):
    return await parse_to_range(date_to=data.date_to, date_from=data.date_from, currency_id=data.currency_id)


