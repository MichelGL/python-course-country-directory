"""
Запуск приложения.
"""

import asyncclick as click

from reader import Reader
from renderer import Renderer


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        country_tab, capital_tab, weather_tab, news_tab = await Renderer(location_info).render()
        click.secho("Информация о стране:")
        click.secho(country_tab, fg="green")
        click.secho("Информация о столице:")
        click.secho(capital_tab, fg="green")
        click.secho("Информация о погоде в столице:")
        click.secho(weather_tab, fg="green")
        click.secho("Последние новости страны:")
        click.secho(news_tab, fg="blue")
    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
