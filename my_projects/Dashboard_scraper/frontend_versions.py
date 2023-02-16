#!/bin/python3
import json
import pprint

import requests
import re

VERSIONS = {"microfrontends": {},
            "frontends": {}}

config_result = requests.get("https://")
response = config_result.content
data = json.loads(response.decode('utf-8'))


def to_pascal_case(s: str) -> str:
    def toupper(match):
        return match.group(1).upper()

    name = re.sub(r'-([A-Za-z])', toupper, s)
    return name


def new_frontend_urls():
    prefix = data["containerFrontendUrl"]
    sufix_dict = data["newFrontendUrls"]
    sufixes = list(sufix_dict.values())

    for sufix in sufixes:
        if sufixes.index(sufix) > 0:
            if sufix == '/':
                continue
            url = f'{prefix}{sufix}/version.json'
            url_result = requests.get(url)
            version = url_result.json()["version"]

            x = sufix.replace('/', '')
            x = to_pascal_case(x)

            VERSIONS["microfrontends"][x] = version

    return VERSIONS


new_frontend_urls()


def frontened_url() -> dict:
    frontendUrls = data["frontendUrls"]
    frontend_values = list(frontendUrls.values())[:-1]
    frontend_keys = list(frontendUrls.keys())[:-1]

    for value in frontend_values:
        if frontend_values.index(value) > 0:
            url = f'{value}/version.json'
            url_result = requests.get(url)
            versions = url_result.json()["version"]

            x = value.split('.')

            for elem in x:
                key = to_pascal_case(elem)
                if key in frontend_keys:
                    keys = key

                    VERSIONS["frontends"][keys] = versions

    return VERSIONS


frontened_url()

pprint.pp(VERSIONS)
