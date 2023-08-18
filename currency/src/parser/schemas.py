from pydantic import BaseModel, Field, validator

from currency.src.parser.utils import validate_date


class ValueCurrencyRangeSchema(BaseModel):
    Date: str
    Value: str


class ValueCurrencySchema(BaseModel):
    Name: str
    Value: str
    ID: str


class RangeCurrencySchema(BaseModel):
    currency_id: str
    date_to: str = Field(..., example='15/08/2023')
    date_from: str = Field(..., example='19/08/2023')

    @validator('date_to', pre=True, allow_reuse=True)
    def validate_date_to(cls, value):
        return validate_date(value)

    @validator('date_from', pre=True, allow_reuse=True)
    def validate_date_from(cls, value, **kwargs):
        return validate_date(value)

