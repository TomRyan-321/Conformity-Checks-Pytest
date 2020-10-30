import pytest
import requests
import os

# CC Region  + API Key
CC_REGION = os.environ.get("CC_REGION", "us-west-2")
CC_APIKEY = os.environ.get("CC_APIKEY")

# Checks API Filters
CC_ACCOUNTIDS = os.environ.get("CC_ACCOUNTIDS")
CC_RISK_LEVELS = os.environ.get("CC_RISKLEVELS", "EXTREME,VERY_HIGH,HIGH,MEDIUM,LOW")

# Limits_allowed_before_failing_tests
MAX_TOTAL = int(os.environ.get("MAX_TOTAL", 0))
MAX_EXTREME = int(os.environ.get("MAX_EXTREME", 0))
MAX_VERY_HIGH = int(os.environ.get("MAX_VERY_HIGH", 0))
MAX_HIGH = int(os.environ.get("MAX_HIGH", 0))
MAX_MEDIUM = int(os.environ.get("MEDIUM", 0))
MAX_LOW = int(os.environ.get("MEDIUM", 0))

url = (
    "https://"
    + CC_REGION
    + "-api.cloudconformity.com/v1/checks?accountIds="
    + CC_ACCOUNTIDS
    + "&filter[riskLevels]="
    + CC_RISK_LEVELS
    + "&page[size]=1000&filter[statuses]=FAILURE"
)

payload = {}
headers = {
    "Content-Type": "application/vnd.api+json",
    "Authorization": "ApiKey " + CC_APIKEY,
}
response = requests.get(url, headers=headers, data=payload)
response_json = response.json()


def test_api_status_code_equals_200():
    assert response.status_code == 200


def test_total_failures_exceed_limit():
    assert response_json["meta"]["total"] <= MAX_TOTAL


def test_extreme_failures_exceed_limit():
    assert (
        sum(
            1
            for c in response_json["data"]
            if c["attributes"]["risk-level"] == "EXTREME"
        )
        <= MAX_EXTREME
    )


def test_very_high_failures_exceed_limit():
    assert (
        sum(
            1
            for c in response_json["data"]
            if c["attributes"]["risk-level"] == "VERY_HIGH"
        )
        <= MAX_VERY_HIGH
    )


def test_high_failures_exceed_limit():
    assert (
        sum(1 for c in response_json["data"] if c["attributes"]["risk-level"] == "HIGH")
        <= MAX_HIGH
    )


def test_medium_failures_exceed_limit():
    assert (
        sum(
            1
            for c in response_json["data"]
            if c["attributes"]["risk-level"] == "MEDIUM"
        )
        <= MAX_MEDIUM
    )


def test_low_failures_exceed_limit():
    assert (
        sum(1 for c in response_json["data"] if c["attributes"]["risk-level"] == "LOW")
        <= MAX_LOW
    )
