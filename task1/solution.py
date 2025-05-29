"""
Необходимо реализовать декоратор @strict
Декоратор проверяет соответствие типов переданных в вызов функции
аргументов типам аргументов, объявленным в прототипе функции.
(подсказка: аннотации типов аргументов можно получить из атрибута
объекта функции func.__annotations__ или с помощью модуля inspect)
При несоответствии типов бросать исключение TypeError
Гарантируется, что параметры в декорируемых функциях
будут следующих типов: bool, int, float, str
Гарантируется, что в декорируемых функциях не будет
значений параметров, заданных по умолчанию
"""
import inspect



def strict(func):
    def wrapper(*args):
        signature = inspect.signature(func)
        bound = signature.bind(*args)

        for name, value in bound.arguments.items():
            expected_type = func.__annotations__.get(name)
            if expected_type and type(value) is not expected_type:
                raise TypeError(f'Argument "{name}" must be {expected_type.__name__}, got {type(value).__name__}')

        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
