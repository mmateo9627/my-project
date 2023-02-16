#!/bin/python3

from requests_html import HTMLSession
# import json
# import pandas as pd
import pprint
s = HTMLSession()

headers = {
    'User-Agent': '',
    'Host': '',
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

#tworzy json file
# with open('table.json', 'w') as f:
#     json.dump(result, f)

#panda zwraca cala tabele w wierszu
# with open('table.json', 'r', encoding='utf-8') as t:
#     data = json.loads(t.read())
# df = pd.json_normalize(data)
    # print(df)
    return result

result = create_tab(s, headers)
def finder(result):
    x = result
    env_keys = ['env', 'env2', 'env3']
    final_dict = {elem: {} for elem in env_keys}
    # print(final_dict)
    for elem in x:
        for env in env_keys:
            final_dict[env][elem['Service']] = elem[env]
# print(final_dict)

   # print(final_dict['test-eu1'])
    # for env, values in final_dict.items():
    #     print(env)
    #     print(values)
    pprint.pp(final_dict)


finder(result)


###
# def finder(result):
#     result_json = json.loads(json.dumps(result))
# #wyszukiwarka1
#     for service in result_json:
#         if service['Service'] == 'SystemMaintenance':
#             print(service['pre-ap1'])

    # finder(result)
