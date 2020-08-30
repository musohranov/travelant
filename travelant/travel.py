"""
Расчет карты доступного путешествия муравья.

* Муравей может передвигаться только вверх, вниз, влево, вправо
* Правила доступности ячейки регулируется из вне (в том числе отрицательные координаты и т.д.)

Алгоритм:
1. На итерации вычисляются соседние доступные ячейки (и не добавленные еще в общую карту путешествия)
2. Если на итерации, кол-во вычисленных доступных ячейек не пусто, итерация повторяется для вычисленного списка ячеек
3. Каждую итерацию кол-во вычисленных доступных ячеек добавляется в общую карту путешествия
"""

from typing import Callable, Set, Tuple

_CellType = Tuple[int, int]
_CellSetType = Set[_CellType]


def get_map(start_point: _CellType,
            check_availability_cell: Callable[[_CellType], bool]) -> _CellSetType:
    """
    Получить карту путешествия

    :param start_point: Стартовая точка путишествия
    :param check_availability_cell: Проверка доступности ячейки

    :return: Множество доступных для перемещения ячеек карты
    """

    travel_map = set()
    last_cells = {start_point, }

    while last_cells:
        adjacent_cells = set()

        for cell in last_cells:
            for adjacent_cell in _get_adjacent_cells(cell):
                if adjacent_cell not in travel_map and check_availability_cell(adjacent_cell):
                    travel_map.add(adjacent_cell)
                    adjacent_cells.add(adjacent_cell)

        last_cells = adjacent_cells

    return travel_map


def _get_adjacent_cells(cell: _CellType) -> _CellSetType:
    """
    Получить соседние ячейки
    :param cell: Ячейка
    """

    return {
        (cell[0] - 1, cell[1]),
        (cell[0] + 1, cell[1]),
        (cell[0], cell[1] - 1),
        (cell[0], cell[1] + 1)
    }


def get_map_with_sum_digits_limit(
        start_point: _CellType,
        max_sum_digits: int,
        add_travel_cells_handler: Callable[[_CellSetType], None] = None) -> _CellSetType:
    """
    Получить карту путешествия вычисленной с ограничением "по сумме цифр координат"

    :param start_point: Стартовая точка путешествия
    :param max_sum_digits: Максимальное значение суммы цифр координат ячейки
    :param add_travel_cells_handler: Обработчик итераций добавления достпынх ячеек

    :return: Множество доступных для перемещения ячеек карты
    """

    if max_sum_digits <= 0:
        raise Exception(f'Значение максимума суммы цифр координат "{max_sum_digits}" должна быть больше 0!')

    def _check_availability_cell(cell: _CellType) -> bool:
        """
        Ячейка доступна если сумма цифр координат <= лимита
        :param cell: Ячейка
        """
        return (_sum_digits(cell[0]) + _sum_digits(cell[1])) <= max_sum_digits

    return get_map(start_point, _check_availability_cell)


def _sum_digits(number: int) -> int:
    """
    Получить сумму цифр числа
    :param number: Число
    """
    n = abs(number)

    s = 0
    while n:
        s += n % 10
        n //= 10
    return s
