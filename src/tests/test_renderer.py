"""
Тестирование функций генерации выходных данных.
"""
import pytest
from collectors.models import (
    CountryDTO,
    CurrencyInfoDTO,
    LanguagesInfoDTO,
    LocationInfoDTO,
    NewsInfoDTO,
    WeatherInfoDTO,
)
from renderer import Renderer


@pytest.mark.asyncio
class TestRenderer:
    location = LocationInfoDTO(
        location=CountryDTO(
            alpha2code="RU",
            capital="Moscow",
            currencies={CurrencyInfoDTO(code="USD")},
            languages={LanguagesInfoDTO(name="Russian", native_name="Русский")},
            flag="test",
            subregion="test",
            name="Russia",
            population=3,
            area=3,
            longitude=3,
            latitude=3,
            alt_spellings=["test"],
            timezones=[3],
        ),
        weather=WeatherInfoDTO(
            timezone=3,
            temp=3,
            pressure=3,
            humidity=3,
            wind_speed=3,
            visibility=3,
            dt=1,
            description="test",
        ),
        currency_rates={"USD": 1.0},
        news=[
            NewsInfoDTO(
                author="test",
                title="test",
                description="test",
                url="test",
                publishedAt="test",
            )
        ],
    )

    async def test_format_languages(self):
        renderer = Renderer(self.location)
        result = await renderer._format_languages()
        assert result == "Russian (Русский)"

    async def test_format_currencies_rates(self):
        renderer = Renderer(self.location)
        result = await renderer._format_currency_rates()
        assert result == "USD = 1.00 руб."