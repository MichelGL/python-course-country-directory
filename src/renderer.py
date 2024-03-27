"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from collectors.models import LocationInfoDTO
from prettytable import PrettyTable
import datetime

class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[PrettyTable, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        country_tab = PrettyTable(["Поле", "Значение"], align="l")
        capital_tab = PrettyTable(["Поле", "Значение"], align="l")
        weather_tab = PrettyTable(["Поле", "Значение"], align="l")

        country_tab.add_row(["Страна", f"{self.location_info.location.name}"])
        country_tab.add_row(["Площадь", f"{self.location_info.location.area} км²"])
        country_tab.add_row(["Регион", f"{self.location_info.location.subregion}"])
        country_tab.add_row(["Языки", f"{await self._format_languages()}"])
        country_tab.add_row(["Население", f"{await self._format_population()} чел."])
        country_tab.add_row(["Курсы валют", f"{await self._format_currency_rates()}"])

        capital_tab.add_row(["Столица", f"{self.location_info.location.capital}"])
        capital_tab.add_row(["Широта", f"{self.location_info.location.latitude}"])
        capital_tab.add_row(["Долгота", f"{self.location_info.location.longitude}"])
        capital_tab.add_row(["Часовой пояс", f"{await self._get_timezone()}"])
        capital_tab.add_row(["Время", f"{await self._format_current_time()}"])

        weather_tab.add_row(["Температура", f"{self.location_info.weather.temp} °C"])
        weather_tab.add_row(["Погода", f"{self.location_info.weather.description}"])
        weather_tab.add_row(["Влажность", f"{self.location_info.weather.humidity}%"])
        weather_tab.add_row(["Видимость", f"{self.location_info.weather.visibility}"])
        weather_tab.add_row(["Скорость ветра", f"{self.location_info.weather.wind_speed} м/с"])

        return country_tab, capital_tab, weather_tab

        # return (
        #     f"Страна: {self.location_info.location.name}",
        #     f"Столица: {self.location_info.location.capital}",
        #     f"Регион: {self.location_info.location.subregion}",
        #     f"Языки: {await self._format_languages()}",
        #     f"Население страны: {await self._format_population()} чел.",
        #     f"Курсы валют: {await self._format_currency_rates()}",
        #     f"Площадь страны: {self.location_info.location.area} км2",
        #     f"Широта столицы: {self.location_info.location.latitude}",
        #     f"Долгота столицы: {self.location_info.location.longitude}",
        #     f"Температура: {self.location_info.weather.temp} °C",
        #     f"Погода: {self.location_info.weather.description}",
        #     f"Влажность: {self.location_info.weather.humidity}%",
        #     f"Видимость: {self.location_info.weather.visibility}",
        #     f"Скорость ветра: {self.location_info.weather.wind_speed} м/с",
        #     f"Время в столице: {await self._format_current_time()}",
        #     f"Часовой пояс столицы: {await self._get_timezone()}",
        # )

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )

    async def _get_timezone(self) -> str:
        """
        Форматирование информации о времени.
        :return:
        """
        hours = self.location_info.weather.timezone / 3600.0
        return "UTC{:+d}:{:02d}".format(int(hours), int((hours % 1) * 60))

    async def _format_current_time(self) -> str:
        """
        Форматирование информации о времени.
        :return:
        """
        dt = datetime.datetime.now() + datetime.timedelta(
            seconds=self.location_info.weather.timezone
        )
        return dt.strftime("%X, %x")
