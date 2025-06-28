import functools
import time

def retry(max_retries, wait_time):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                     func(*args, **kwargs)
                except DBConnectionError as e:
                    time.sleep(5)
            raise DBConnectionError(f"retried {max_retries} times, could not connect to database. Aborting the job")
        return wrapper
    return decorator

@retry(max_retries=5, wait_time=1)
def example_function():
    # function that may raise an exception
    raise DBConnectionError("error occured")


class DBConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)

example_function()
