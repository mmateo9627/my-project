#!/bin/python3

from requests_html import HTMLSession
import json

s = HTMLSession()

headers = {
    'User-Agent': '',
    'Host': "",
}

def create_tab(s, headers):
    res = s.get('https://', headers=headers)

    table = res.html.find('table')[0]

# for row in table.find('tr'):
#     for c in row.find('td'):
#         print(c.text)
#to samo co wyzej tylko bardziej pythonowo
    tabledata = [[c.text for c in row.find('td')] for row in table.find('tr')]

    tableheader = [[c.text for c in row.find('th')] for row in table.find('tr')][0]

    result = [dict(zip(tableheader, t)) for t in tabledata[2:]]

# with open('table.json', 'w') as f:
    #     json.dump(resoult, f)
    return result

result = create_tab(s, headers)

def finder(result):
    result_json = json.loads(json.dumps(result))

    for service in result_json:
        if service['Service'] == 'xyz':
            print(service['x'])

finder(result)
