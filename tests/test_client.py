import pytest
import responses

from speedtesttrackerapi import ApiClient
from speedtesttrackerapi.exceptions import AuthenticationError

BASE_URL = "https://speedtest-tracker.example.com"
TOKEN = "token"


@responses.activate
def test_get_statistics_success():
    responses.add(
        responses.GET,
        f"{BASE_URL}/api/v1/stats",
        json={
            "data": {
                "ping": {"avg": 19.26, "min": 11.76, "max": 374.67},
                "download": {
                    "avg": 36141788,
                    "avg_bits": 289134304,
                    "avg_bits_human": "289.13 Mbps",
                    "min": 11328164,
                    "min_bits": 90625312,
                    "min_bits_human": "90.63 Mbps",
                    "max": 40171848,
                    "max_bits": 321374784,
                    "max_bits_human": "321.37 Mbps",
                },
                "upload": {
                    "avg": 18176256,
                    "avg_bits": 145410045,
                    "avg_bits_human": "145.41 Mbps",
                    "min": 223188,
                    "min_bits": 1785504,
                    "min_bits_human": "1.79 Mbps",
                    "max": 20316598,
                    "max_bits": 162532784,
                    "max_bits_human": "162.53 Mbps",
                },
                "total_results": 1223,
            },
            "message": "ok",
        },
        status=200,
    )

    client = ApiClient(BASE_URL, TOKEN, verify_ssl=False)
    response = client.get_statistics()

    assert response.message == "ok"
    assert response.data.total_results == 1223
    assert response.data.ping.avg == 19.26
    assert response.data.download.avg_bits_human == "289.13 Mbps"


@responses.activate
def test_get_statistics_401_raises_auth_error():
    responses.add(
        responses.GET,
        f"{BASE_URL}/api/v1/stats",
        json={"message": "Unauthorized"},
        status=401,
    )

    client = ApiClient(BASE_URL, TOKEN, verify_ssl=False)

    with pytest.raises(AuthenticationError):
        client.get_statistics()
