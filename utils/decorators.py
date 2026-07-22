import functools


def log_function_name(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\033[96mExecuting function: {func.__name__}\033[0m")
        return func(*args, **kwargs)
    return wrapper