#!/usr/bin/python3

import requests
import json
import os
import datetime

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

start_time = datetime.datetime(2016, 8, 14, 9, 0, 0)


def get_time(time):
    time = str(datetime.datetime.fromtimestamp(time) - start_time)
    return time.split('.')[0]


def download(url):
    result = session.request('GET', url)
    if (result.status_code != 200):
        print(url, result.status_code)
    return json.loads(result.text)


def print_submission(submit):
    part = submit["participant"]
    score = submit['score']
    time = submit['time']
    total = sum(submit['extra'])
    problem = submit["task"]
    print("[" + get_time(time) + "]", part, "[" + participants[part] + "]", problems[problem], score, total)
    os.system("notify-send '[%s] %s submited %s for %d points (now have %d)'" % (get_time(time), participants[part], problems[problem], score, total))


print('Updating')

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
