"""Client class for the SpeedtestTrackerAPI Package"""

import requests
from .exceptions import ApiError, AuthenticationError, ResourceNotFoundError
from .models import (
    ResultResponse,
    ResultsCollection,
    ServersCollection,
    SpeedtestRun,
    Stats,
    QueryParameters,
)


class ApiClient:
    """"""

    def __init__(self, base_url: str, token: str, verify_ssl: bool = True):
        """Initializes the api client

        :param base_url: the base URL of the api (e.g. 'https://speedtest-tracker.example.com)
        :param token: api token for authentication
        :param verify_ssl: True for verifying the ssl certificate, False for ignoring
        """
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()

    def _request(
        self, method: str, endpoint: str, params: dict = None, **kwargs
    ) -> dict:
        """Internal helping wrapper, which runs all http requests and filters errors"""
        if endpoint.startswith(("http://", "https://")):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                verify=self.verify_ssl,
                params=params,
                **kwargs,
            )
            if response.status_code in (401, 403):
                raise AuthenticationError(f"Authentification failed: {response.text}")
            elif response.status_code == 404:
                raise ResourceNotFoundError(f"Emdpoint or resource not found: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.SSLError as e:
            raise ApiError(
                f"SSL Certificate Error. Set 'verify_ssl = False', if you want to skip ssl verification. Details: {e}"
            )
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Network or Connection Error: {e}")

    def get_results(self, params: QueryParameters = None) -> ResultsCollection:
        """Gets results from endpoint /api/v1/results"""
        return ResultsCollection.model_validate(
            self._request("GET", "/api/v1/results", params)
        )

    def get_result_by_id(self, id: int) -> ResultResponse:
        """Gets a result from endpoint /api/v1/results/{id} by its id"""
        return ResultResponse.model_validate(
            self._request("GET", f"/api/v1/results/{id}")
        )

    def get_latest_result(self) -> ResultResponse:
        """Gets latest result from endpoint /api/v1/results/latest"""
        return ResultResponse.model_validate(
            self._request("GET", "/api/v1/results/latest")
        )

    def run_speedtest(self, params: QueryParameters = None) -> SpeedtestRun:
        """Uses the /api/v1/speedtests/run endpoint to run a new Ookla speedtest and get its data."""
        return SpeedtestRun.model_validate(
            self._request("POST", "/api/v1/speedtests/run", params)
        )

    def get_speedtest_server_list(self) -> ServersCollection:
        """Gets a list of available Ookla speedtest servers from endpoint /api/v1/speedtests/list-servers"""
        return ServersCollection.model_validate(
            self._request("GET", "/api/v1/speedtests/list-servers")
        )

    def get_statistics(self, params: QueryParameters = None) -> Stats:
        """Gets aggregated speedtest statistics from endpoint /api/v1/stats"""
        return Stats.model_validate(self._request("GET", "/api/v1/stats", params))

    def get_ookla_server_list(self) -> ServersCollection:
        """Gets a list of available Ookla speedtest servers from endpoint /api/v1/ookla/list-servers"""
        return ServersCollection.model_validate(
            self._request("GET", "/api/v1/ookla/list-servers")
        )
