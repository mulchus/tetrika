def strict(func):
    def wrapper(*args, **kwargs):
        zipped_vars = zip((list(args) + list(kwargs.values())), list(func.__annotations__.values()))
        for zipped_var in zipped_vars:
            if not isinstance(zipped_var[0], zipped_var[1]):
                raise TypeError
        return func(*args, **kwargs)
    return wrapper

@strict
def sum_two(a: int, b: int, c: str) -> int:
    return a + b + int(c)

print(sum_two(1, 2, c='1'))  # >>> 3
print(sum_two(1, 2.4, c='.1'))  # >>> TypeError
