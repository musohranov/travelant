import unittest

from parameterized import parameterized

from travel import get_map, _get_adjacent_cells, get_map_with_sum_digits_limit, _sum_digits


class GetMap(unittest.TestCase):
    def test_base(self):
        """
        Базовый сценарий
        В идеале необходимо убедится что начиная со стартовой точки выполняется поиск соседей, а затем
        для найденных соседей снова выполнен поиск соседей и т.д. Но сделаем проще и проверим результат.
        """

        # Ограничимся квадратом (-1, -1) - (1, 1)
        result = get_map((0, 0), lambda cell: abs(cell[0]) <= 1 and abs(cell[1]) <= 1)
        self.assertEqual(result, {(-1, -1), (-1, 0), (-1, 1),
                                  (0, -1), (0, 0), (0, 1),
                                  (1, -1), (1, 0), (1, 1)})

    @parameterized.expand([
        ((0, 0), {(-1, 0), (1, 0), (0, -1), (0, 1)}),
    ])
    def test_get_adjacent_cells(self, cell, result):
        """
        Проверить получение соседнгих ячеек
        :param cell: Ячейка
        :param result: Результат
        """

        self.assertEqual(_get_adjacent_cells(cell), result)


class GetMapWithSumDigitsLimit(unittest.TestCase):
    def test_fail(self):
        """
        Краевые условия
        """

        try:
            get_map_with_sum_digits_limit((0, 0), -1)
        except Exception as err:
            self.assertEqual(str(err), f'Значение максимума суммы цифр координат "-1" должно быть больше 0!')
        else:
            self.fail()

    def test_base(self):
        """
        Базовый сценарий
        """

        result = get_map_with_sum_digits_limit((0, 0), 1)
        self.assertEqual(result, {(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)})


class SumDigits(unittest.TestCase):
    @parameterized.expand([
        (0, 0),
        (123, 6),
        (-123, 6),
    ])
    def test_0(self, number, result):
        """
        Базовый сценарий
        :param number: Число
        :param result: Результат
        """

        self.assertEqual(_sum_digits(number), result)


if __name__ == '__main__':
    unittest.main()
