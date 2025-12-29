import logging
from time import perf_counter
from functools import lru_cache  # кеширование результатов

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fib")


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n должно быть >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_rec_plain(n: int) -> int:
    # рекурсия без кэша: очень много повторных вычислений
    if n < 0:
        raise ValueError("n должно быть >= 0")
    if n < 2:
        return n
    return fib_rec_plain(n - 1) + fib_rec_plain(n - 2)


@lru_cache(maxsize=None)
def fib_rec_cached(n: int) -> int:
    # рекурсия с кэшем: уже посчитанные значения берутся из памяти
    if n < 0:
        raise ValueError("n должно быть >= 0")
    if n < 2:
        return n
    return fib_rec_cached(n - 1) + fib_rec_cached(n - 2)


def time_call(func, n: int):
    start = perf_counter()
    result = func(n)
    # простой замер "после - до"
    elapsed = perf_counter() - start
    return result, elapsed

def sum_nested(data) -> int:
    # сумма всех чисел во вложенном списке
    total = 0
    for item in data:
        # если это список — считаем его сумму рекурсивно
        if isinstance(item, list):
            total += sum_nested(item)
        # если это число — добавляем
        else:
            total += item
    return total



if __name__ == "__main__":
    #сюда можно подставить необходимые значения
    n = 50
    n1=13

    val_i, t_i = time_call(fib_iter, n)
    logger.info(f"итеративная функия подсчёта чисел фибоначчи от ({n}) = {val_i}, значение вычислялось {t_i:.6f} секунд")

    # будет очень медленно для n=50, поэтому берем число для которого время подсчёта
    # будет примерно таким же как и у других функций для 50
    val_plain, t_plain = time_call(fib_rec_plain, n1)
    logger.info(f"рекурсивная функия подсчёта чисел фибоначчи без кэширования от ({n1}) = {val_plain}, значение вычислялось {t_plain:.6f} секунд")

    #очищаем кэш функции чтобы замер был с нуля
    fib_rec_cached.cache_clear()
    val_cached, t_cached = time_call(fib_rec_cached, n)
    logger.info(f"рекурсивная функия подсчёта чисел фибоначчи с кэшированием от ({n}) = {val_cached}, значение вычислялось {t_cached:.6f} секунд")

    #все три способа должны дать один и тот же ответ, но проверяем только два
    # тк рекурсия без кэширования будет вычисляться очень долго
    assert val_i == val_cached

    lst = [1, [2, 3], [4, [5, 6]], [-1, -5], 0]
    print(f"сумма всех чисел списка {lst} = {sum_nested(lst)}")

