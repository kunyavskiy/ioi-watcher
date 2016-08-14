#!/usr/bin/python3

import requests
import json
import os

session = requests.session()

problems = {
    '1': 'moluecula',
    '2': 'railroad',
    '3': 'shortcut'
}

participants = {
    'RUS-1': 'Vladislav Makeev',
    'RUS-2': 'Stanislav Naumov',
    'RUS-3': 'Mikhail Putilin',
    'RUS-4': 'Grigoriy Reznikov',
    'RU2-1': 'Mikhail Anoprenko',
    'RU2-2': 'Alexandra Drozdova',
    'RU2-3': 'Askhat Sakhabiev',
    'RU2-4': 'Denis Solnkov'
}


def download(url):
    print(url, end=' ')
    result = session.request('GET', url)
    print(result.status_code)
    return json.loads(result.text)


def print_submission(submit):
    part = submit["participant"]
    score = sum(submit['extra'])
    problem = submit["task"]
    print(part, problems[problem], score)
    os.system("notify-send '%s submited %s for %d points'" % (participants[part], problems[problem], score))


try:
    data = json.load(open("data.json"))
except FileNotFoundError:
    data = []

for i in participants.keys():
    part_data = download('http://pcms.ioi2016.ru/sublist/' + i)
    for submit in part_data:
        submit["participant"] = i
        if submit not in data:
            print_submission(submit)
        data.append(submit)

open("data.json", 'w').write(json.dumps(data))
