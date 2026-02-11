import requests
import requests.packages
# from json import JSONDecodeError TODO: remove if runtime experiment on model_validate_json() is successful
from objekt_api.exceptions import ObjektApiException
from typing import Dict
import logging

class ObjektResponse:
    def __init__(self, data: bytes, status_code: int, message: str = ''):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data

class ObjektHTTP:
    def __init__(self, api_key: str = '', ssl_verify: bool = True, logger: logging.Logger = None):
        """
        :param api_key: (unnecessary) in case the objekt api ever requires an api key to get information
        :param ssl_verify: True by default, can disable if there are SSL issues by setting to False
        :param logger: (optional) pass in your own logger if your application has one 
        """

        self.url = "https://objekt.top/api"
        self._api_key = api_key
        self._logger = logger or logging.getLogger(__name__)
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()
    
    def get(self, endpoint: str, params: Dict = None) -> ObjektResponse:
        """
        :param endpoint: The endpoint you would like to hit from objekt's api
        """

        full_url = self.url + endpoint

        log_line_pre = f"method = GET, url = {full_url}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            print(log_line_pre)
            response = requests.get(url=full_url, verify=self._ssl_verify, params=params)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise ObjektApiException("Request failed") from e

        data = response.content

        """
        try:
            data = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise ObjektApiException("Bad JSON in response") from e
        """

        is_success = response.status_code >= 200 and response.status_code <= 299
        log_line = log_line_post.format(is_success, response.status_code, response.reason)

        if is_success:
            self._logger.debug(msg=log_line)
            return ObjektResponse(status_code = response.status_code, message = response.reason, data = data)
        self._logger.error(msg=log_line)
        raise ObjektApiException(f"{response.status_code}: {response.reason}")
