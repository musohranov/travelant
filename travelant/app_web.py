"""
Веб сервер получения карты путешествия.
Страница по умолчанию содержит инструкция по использованию. Входные данные задаются в качестве параметров GET запроса.
"""

from typing import Tuple, Set
import traceback

from aiohttp import web
import aiohttp_jinja2
import jinja2

from travel import get_map_with_sum_digits_limit

#
routes = web.RouteTableDef()


@routes.get('/')
async def get_map(request: web.Request) -> web.Response:
    """
    Обработчик запроса получения карты путешествия
    :param request: Запрос.
    :return: Если при обработке запроса возникла ошибока,
    возвращаем страницу 'help', иначе запрашиваемый результат
    """

    try:
        if not request.query:
            return render_help(request)

        start_point = (int(request.query['x']), int(request.query['y']))
        sum_digits = int(request.query['s'])

        travel_map = get_map_with_sum_digits_limit(start_point, sum_digits)

        if 'onlynumber' in request.query:
            # Отобразить численный результат
            return web.Response(text=str(len(travel_map)))

        # Отобразить графический результат
        return render_map(request, start_point, sum_digits, travel_map)
    except:
        return render_help(request, traceback.format_exc())


def render_help(request: web.Request, error: str = None) -> web.Response:
    """
    Отобразить страницу помощи
    :param request: Запрос
    :param error: Текст ошибки
    """

    return aiohttp_jinja2.render_template('help.jinja2', request, {'error': error})


def render_map(request: web.Request,
               start_point: Tuple[int, int],
               sum_digits: int,
               travel_map: Set[Tuple[int, int]]) -> web.Response:
    """
    Отобразить страницу карты

    :param request: Запрос
    :param start_point: Стартовая точка путешествия
    :param sum_digits: Максимальное значение суммы цифр координат ячейки
    :param travel_map: Карта путешествия
    """

    min_x, min_y = start_point
    max_x, max_y = start_point

    for cell in travel_map:
        min_x = min(min_x, cell[0])
        min_y = min(min_y, cell[1])
        max_x = max(max_x, cell[0])
        max_y = max(max_y, cell[1])

    return aiohttp_jinja2.render_template(
        'map.jinja2',
        request,
        {'cell_list': travel_map,
         'start_point': start_point,
         'min_x': min_x, 'min_y': min_y, 'max_x': max_x, 'max_y': max_y,
         'sum_digits': sum_digits})


#
# Запуск web сервера
#

app = web.Application()

app.add_routes(routes)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('app_web_templates'))

web.run_app(app)
