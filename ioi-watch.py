#!/usr/bin/python3

import datetime
import json
import os
import requests

session = requests.session()

problems = {
    'nowruz': 'nowruz',
    'wiring': 'wiring',
    'train': 'train',
}

fmt = {
    'nowruz' : '%.2f',
}

subscore = dict()

participants = {
    'RUS_2d4': 'Denis  Shpakovskii',
    'RUS_2d1': 'Aleksandra Drozdova',
    'RUS_2d2': 'Egor  Lifar',
    'RUS_2d3': 'Vladimir Romanov',
}

start_time = datetime.datetime(2017, 7, 30, 7, 30, 0)


def get_time(time):
    time = str(datetime.datetime.fromtimestamp(time) - start_time)
    return time.split('.')[0]


def download(url):
    result = session.request('GET', url)
    if result.status_code != 200:
        print(url, result.status_code)
    return json.loads(result.text)

def getFmt(problem):
    return '%d' if problem not in fmt else fmt[problem]

def print_submission(submit):
    part = submit["participant"]
    if part not in subscore:
      subscore[part] = dict();
    problem = submit["task"]
    score = submit['score']
    if problem not in subscore[part]:
      subscore[part][problem] = list(map(float, submit['extra']))
    else:
      for i in range(len(submit['extra'])):
        subscore[part][problem][i] = max(subscore[part][problem][i], float(submit['extra'][i]))
    total = sum(subscore[part][problem])
    time = submit['time']
    print("[" + get_time(time) + "]", part, "[" + participants[part] + "]", problems[problem], score, total)
    os.system(("notify-send '[%s] %s submited %s for " + getFmt(problem) + " points (now have " + getFmt(problem) + ")'") %
              (get_time(time), participants[part], problems[problem], score, total))


print('Updating')

try:
    data = json.load(open("data.json"))
except FileNotFoundError:
    data = []

for i in participants.keys():
    part_data = download('http://scoreboard.ioi2017.org/sublist/' + i)
    for submit in part_data:
        submit["participant"] = i
        if submit not in data:
            print_submission(submit)
        data.append(submit)

open("data.json", 'w').write(json.dumps(data))
