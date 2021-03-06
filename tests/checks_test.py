import os
import pytest
import requests

# Conformity Region, API Key & Target Account(s) variables
CC_REGION = os.environ.get("CC_REGION", "us-west-2")
CC_APIKEY = os.environ["CC_APIKEY"]
CC_ACCOUNTIDS = os.environ["CC_ACCOUNTIDS"]

# Pagination variables
CC_PAGESIZE = int(os.environ.get("CC_PAGESIZE", 1000))
CC_PAGENUMBER = int(os.environ.get("CC_PAGENUMBER", 0))

# Checks API Filters
CC_FILTER_CATEGORIES = os.environ.get("CC_FILTER_CATEGORIES", "")
CC_FILTER_COMPLIANCES = os.environ.get("CC_FILTER_COMPLIANCES", "")
CC_FILTER_CREATEDLESSTHAN = os.environ.get("CC_FILTER_CREATEDLESSTHAN", "")
CC_FILTER_CREATEDMORETHAN = os.environ.get("CC_FILTER_CREATEDMORETHAN", "")
CC_FILTER_NEWERTHANDAYS = os.environ.get("CC_FILTER_NEWERTHANDAYS", "")
CC_FILTER_OLDERTHANDAYS = os.environ.get("CC_FILTER_OLDERTHANDAYS", "")
CC_FILTER_REGIONS = os.environ.get("CC_FILTER_REGIONS", "")
CC_FILTER_RESOURCE = os.environ.get("CC_FILTER_RESOURCE", "")
CC_FILTER_RISKLEVELS = os.environ.get("CC_FILTER_RISKLEVELS", "")
CC_FILTER_RULEIDS = os.environ.get("CC_FILTER_RULEIDS", "")
CC_FILTER_SERVICES = os.environ.get("CC_FILTER_SERVICES", "")
CC_FILTER_STATUSES = os.environ.get("CC_FILTER_STATUSES", "FAILURE")
CC_FILTER_TAGS = os.environ.get("CC_FILTER_TAGS", "")

# Limits allowed before failing tests
MAX_TOTAL = int(os.environ.get("MAX_TOTAL", 0))
MAX_EXTREME = int(os.environ.get("MAX_EXTREME", 0))
MAX_VERY_HIGH = int(os.environ.get("MAX_VERY_HIGH", 0))
MAX_HIGH = int(os.environ.get("MAX_HIGH", 0))
MAX_MEDIUM = int(os.environ.get("MAX_MEDIUM", 0))
MAX_LOW = int(os.environ.get("MAX_LOW", 0))

url = "https://" + CC_REGION + "-api.cloudconformity.com/v1/checks"

params = {
    "accountIds": CC_ACCOUNTIDS,
    "filter[categories]": CC_FILTER_CATEGORIES,
    "filter[compliances]": CC_FILTER_COMPLIANCES,
    "filter[createdLessThanDays]": CC_FILTER_CREATEDLESSTHAN,
    "filter[createdMoreThanDays]": CC_FILTER_CREATEDMORETHAN,
    "filter[newerThanDays]": CC_FILTER_NEWERTHANDAYS,
    "filter[olderThanDays]": CC_FILTER_OLDERTHANDAYS,
    "filter[regions]": CC_FILTER_REGIONS,
    "filter[resource]": CC_FILTER_RESOURCE,
    "filter[riskLevels]": CC_FILTER_RISKLEVELS,
    "filter[ruleIds]": CC_FILTER_RULEIDS,
    "filter[services]": CC_FILTER_SERVICES,
    "filter[tags]": CC_FILTER_TAGS,
    "filter[statuses]": CC_FILTER_STATUSES,
    "page[size]": CC_PAGESIZE,
    "page[number]": CC_PAGENUMBER,
}

payload = {}
headers = {
    "Content-Type": "application/vnd.api+json",
    "Authorization": "ApiKey " + CC_APIKEY,
}

session = requests.session()


def get_account_checks():
    combined = []
    counter = 0
    max_results = 1
    while counter <= max_results:
        page = session.get(url, params=params, headers=headers, data=payload).json()
        max_results = page["meta"]["total"]
        counter += CC_PAGESIZE
        params["page[number]"] += 1
        data = page["data"]
        combined += data
    return {"data": combined, "meta": page["meta"]}


response_json = get_account_checks()


def test_total_failures_exceed_limit():
    assert int(response_json["meta"]["total"]) <= MAX_TOTAL


def test_extreme_failures_exceed_limit():
    count = sum(
        1 for c in response_json["data"] if c["attributes"]["risk-level"] == "EXTREME"
    )
    assert count <= MAX_EXTREME


def test_very_high_failures_exceed_limit():
    count = sum(
        1 for c in response_json["data"] if c["attributes"]["risk-level"] == "VERY_HIGH"
    )
    assert count <= MAX_VERY_HIGH


def test_high_failures_exceed_limit():
    count = sum(
        1 for c in response_json["data"] if c["attributes"]["risk-level"] == "HIGH"
    )
    assert count <= MAX_HIGH


def test_medium_failures_exceed_limit():
    count = sum(
        1 for c in response_json["data"] if c["attributes"]["risk-level"] == "MEDIUM"
    )
    assert count <= MAX_MEDIUM


def test_low_failures_exceed_limit():
    count = sum(
        1 for c in response_json["data"] if c["attributes"]["risk-level"] == "LOW"
    )
    assert count <= MAX_LOW
