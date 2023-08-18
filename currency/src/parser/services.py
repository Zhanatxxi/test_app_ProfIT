from datetime import date

import aiohttp
import xmltodict

from fastapi import HTTPException, status

from currency.settings.settings import settings
from currency.src.parser.schemas import ValueCurrencySchema, ValueCurrencyRangeSchema

TO_DAY_DATE = date.today().strftime('%d/%m/%Y')
URL_TO_DAY = f'{settings.BASE_URL}/XML_daily.asp?date_req={TO_DAY_DATE}'


async def parse_to_day() -> list[ValueCurrencySchema]:
    """
    Возаращает список с курсами валют на сегодняшний день
    :return: list[ValueCurrencySchema]
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_TO_DAY) as response:
            if response.status != 200:
                raise HTTPException(detail="Ooops, server not work!!!", status_code=status.HTTP_404_NOT_FOUND)
            xml = await response.text()
            html_to_dict = xmltodict.parse(xml)
            val_curs = html_to_dict["ValCurs"]
            valute = val_curs["Valute"]
            answer = list()
            for item in valute:
                id_value, name, value = filter(lambda key: key in ['@ID', 'Name', 'Value'], item.keys())
                answer.append(ValueCurrencySchema(
                    ID=item[id_value],
                    Name=item[name],
                    Value=item[value]
                ))
            return answer


async def parse_to_range(*, date_to: str, date_from, currency_id: str) -> list[ValueCurrencyRangeSchema]:
    URL_RANGE = f'{settings.BASE_URL}/XML_dynamic.asp?date_req1=' \
                f'{date_to}&date_req2={date_from}&VAL_NM_RQ={currency_id}'

    if currency_id not in [valute.ID for valute in await parse_to_day()]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='currency_id wrong')

    async with aiohttp.ClientSession() as session:
        async with session.get(URL_RANGE) as response:
            if response.status != 200:
                raise HTTPException(detail="Ooops, server not work!!!", status_code=status.HTTP_404_NOT_FOUND)
            xml = await response.text()
            html_to_dict = xmltodict.parse(xml)
            val_curs = html_to_dict["ValCurs"]
            record = val_curs["Record"]
            answer = list()
            if type(record) == list:
                for item in record:
                    date_item, value = filter(lambda key: key in ['@Date', 'Value'], item.keys())
                    answer.append(ValueCurrencyRangeSchema(
                        Date=item[date_item],
                        Value=item[value]
                    ))
            else:
                date_item, value = filter(lambda key: key in ['@Date', 'Value'], record.keys())
                answer.append(ValueCurrencyRangeSchema(
                    Date=record[date_item],
                    Value=record[value]
                ))
            return answer

