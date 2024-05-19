import json
import requests
from datetime import datetime

def getDataFromRequest(link):
    url = requests.get(link)
    data = json.loads(url.text)
    return data

def getMapValue(map, key, classinfo):
    if key in map:
        return map[key]
    else:
        if classinfo == str:
            return ''
        if classinfo == int:
            return 0

def getDate(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date

def getMapMonths():
    months = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10:'Oct',
        11: 'Nov',
        12: 'Dec'
    }
    return months

def getListMonths():
    months = getMapMonths()
    return list(months.keys())

def getMonth(number):
    months = getMapMonths()
    return months[number]

def getDivision(number):
    division = {
        0: 'Others',
        1: 'Div 1',
        2: 'Div 2',
        3: 'Div 3',
        4: 'Div 4'
    }
    return division[number]

def getSolvedTypeColor(solvedType):
    colors = {
        'CONTESTANT': 'gold',
        'PRACTICE': 'mediumturquoise',
        'VIRTUAL': 'darkorange',
        'OUT_OF_COMPETITION': 'lightgreen',
        'MANAGER': '#ff6792' 
    }
    return colors[solvedType]

def getDivisionColor(division):
    colors = {
        'Others': 'lightgreen',
        'Div 1': '#ff6792',
        'Div 2': 'gold',
        'Div 3': 'mediumturquoise',
        'Div 4': 'darkorange'
    }
    return colors[division]

def getVerdictColor(verdict):
    colors = {
        'OK': '#49d1cc',
        'PARTIAL': '#07cc96',
        'COMPILATION_ERROR': '#ac64fa',
        'RUNTIME_ERROR': '#ff98ff',
        'WRONG_ANSWER': '#ff6792',
        'PRESENTATION_ERROR': '#636efb',
        'TIME_LIMIT_EXCEEDED': '#1ad3f3',
        'MEMORY_LIMIT_EXCEEDED': '#ffa25a',
        'CHALLENGED': '#90ef91',
        'SKIPPED': '#ef553b',
        'IDLENESS_LIMIT_EXCEEDED': '#32ffc9',
        'SECURITY_VIOLATED': '#ffe9b7',
        'INPUT_PREPARATION_CRASHED': '#e8f8d6',
        'TESTING': '#ffccdb',
        'FAILED': '#f7a79a',
        'REJECTED': '#c7cafd',
        'CRASHED': '#e1c6fd',
    }
    return colors[verdict]

def getTagColor(tag):
    return 'gold'

def getRatingColor(rating):
    return 'darkorange'
