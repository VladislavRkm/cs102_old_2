import typing as tp

import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        possible_errors = []
        for i in range(400, 600):
            possible_errors.append(i)
        retry_process = Retry(
            allowed_methods=["POST", "GET"],  # задает список разрешенных HTTP-методов,
            total=max_retries,  # задает максимальное количество повторных попыток
            backoff_factor=backoff_factor,  # задает коэффициент задержки между повторными попытками
            status_forcelist=possible_errors,
            # задает список статусов HTTP-ответов, которые приведут к повторному
            # выполнению запроса.
        )
        http_adapter = HTTPAdapter(max_retries=retry_process)
        self.session.mount("https://", http_adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        self.timeout = kwargs.get("timeout", self.timeout)
        full_url = self.base_url + "/" + url
        response = self.session.get(full_url, timeout=self.timeout, *args, **kwargs)
        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        self.timeout = kwargs.get("timeout", self.timeout)
        full_url = self.base_url + "/" + url
        response = self.session.post(full_url, timeout=self.timeout, *args, **kwargs)
        return response
# ok