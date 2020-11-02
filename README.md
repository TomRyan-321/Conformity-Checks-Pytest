# Conformity-Checks-Pytest
A simple set of tests to check the number of failures returned from cloud conformity checks API. Intended to be used as part of a CICD pipeline to verify the number of failures introduced after a build has been deployed.

## Installation

Install the requirements
```
pip3 install -r requirements.txt
```

## Usage

1. Export environment variables relevant to your Cloud Conformity Account `CC_REGION`, `CC_APIKEY`, `CC_ACCOUNTIDS`.
2. Export the Conformity filters you want to run the tests against. Eg `CC_FILTER_CATERGORY=Security`, `CC_FILTER_TAGS=Build::1jh12asd6d`
3. Optionally configure the acceptable failure limits per severity basis by setting the following environment variables. `MAX_TOTAL`, `MAX_EXTREME`, `MAX_VERY_HIGH`, `MAX_HIGH`, `MAX_MEDIUM`, `MAX_LOW`. All of these default to "0".
4. Run pytest

## Full list of Conformity filters available in script:
`CC_FILTER_CATEGORIES`,
`CC_FILTER_COMPLIANCES`,
`CC_FILTER_CREATEDLESSTHAN`,
`CC_FILTER_REGIONS`,
`CC_FILTER_RISKLEVELS`,
`CC_FILTER_SERVICES`,
`CC_FILTER_TAGS`
