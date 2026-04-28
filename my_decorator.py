import time


def check_time(func):
    def wrapper(*args, **kwargs):
        """измеряет скорость выполнения кода"""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"функция {func.__name__} выполнялась {end - start:.6f} секунд")
        return result

    return wrapper


@check_time
def sumnums(numbers):
    return sum(numbers)

@check_time
def say_hello(name):
    print("Привет", name)


res = sumnums(range(1000000000))
print(res)

say_hello("Anton")