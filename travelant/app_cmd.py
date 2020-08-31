"""
Утилита интерфейса командной строки, для расчета кол-ва ячеек карты путешествия.

Пример использования:
> app_cmd.py 1000 1000 25
> 148848
"""

import sys
import traceback

from travel import get_map_with_sum_digits_limit


def run() -> None:
    """
    Запустить утилиту
    """

    try:
        start_point = (int(sys.argv[1]), int(sys.argv[2]))
        sum_digits = int(sys.argv[3])

        print(len(get_map_with_sum_digits_limit(start_point, sum_digits)))
    except:
        print(f'{traceback.format_exc()}\n'
              f'Необходимо указать значения <X:Число> <Y:Число> <Максимальная сумма цифр ячейки>')


if __name__ == '__main__':
    run()
