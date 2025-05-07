import timeit
import logging
from colorama import Fore, Style
from functools import wraps
import time


def precise_sync_timer(number=100, repeat=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(
                Fore.YELLOW
                + f"Запуск '{func.__name__}' {number} раз, повторений: {repeat}."
                + Style.RESET_ALL
            )
            timings = timeit.repeat(
                lambda: func(*args, **kwargs), number=number, repeat=repeat
            )
            best_time = min(timings) / number
            logging.info(
                Fore.GREEN
                + f"Функция '{func.__name__}' - лучшее время: {best_time:.6f} сек (среднее на вызов)."
                + Style.RESET_ALL
            )
            return func(*args, **kwargs)  # Возвращаем результат оригинальной функции

        return wrapper

    return decorator


def precise_async_timer(number=100, repeat=3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logging.info(
                Fore.YELLOW
                + f"Запуск асинхронной функции '{func.__name__}' {number} раз, повторений: {repeat}."
                + Style.RESET_ALL
            )
            timings = []
            for _ in range(repeat):
                start_time = time.perf_counter()
                for _ in range(number):
                    await func(*args, **kwargs)
                end_time = time.perf_counter()
                timings.append(end_time - start_time)

            best_time = min(timings) / number
            logging.info(
                Fore.CYAN
                + f"Асинхронная функция '{func.__name__}' - лучшее среднее время: {best_time:.6f} сек (на вызов)."
                + Style.RESET_ALL
            )
            return await func(
                *args, **kwargs
            )  # Возвращаем результат оригинальной функции

        return wrapper

    return decorator
