from httpx import Timeout, HTTPError


def connect_timeout_pass(func):
    def wrapper(*args, **kwargs):
        for i in range(100):
            try:
                return func(*args, **kwargs)
            except HTTPError:
                pass

    return wrapper


class ApiError(Exception):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class ApiManager:
    base_url: str
    timeout = Timeout(60.0)

    @staticmethod
    def check_status_code(response, success_code=200):
        if response.status_code != success_code:
            raise ApiError(response.status_code, response.text)
