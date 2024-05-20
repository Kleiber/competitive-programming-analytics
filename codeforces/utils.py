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

def getMonth(month):
    return monthMap[month]

def getDivision(division):
    return divisionMap[division]

def getRankName(rank):
   if rank == 0:
    return 'Without Rating'

    rankChars = list(rank)
    for i in range(0, len(rankChars)):
        if i == 0 or rankChars[i - 1] == ' ':
            rankChars[i] = rankChars[i].upper()

    return ''.join(rankChars)

def getRankColor(rank):
    if rank == 0:
        return 'red'
    return rankMapColor[rank.lower()]

def getSolvedTypeColor(mode):
    return modeSolvedMapColor[mode.upper()]

def getDivisionColor(division):
    return divisionMapColor[division.lower()]

def getVerdictColor(verdict):
    return verdictMapColors[verdict]

def getTagColor(tag):
    index = tagMapColor[tag]
    return colors[index]

def getRatingColor(rating):
    return 'darkorange'

def getRatingColors():
    # rating 0 is the last color
    ratingMapColor = {0: colors[43]}

    index = 0
    for rating in range(800, 3500, 100):
        ratingMapColor[rating] = colors[index]
        index += 1
    return ratingMapColor

colors = ['#ffd701', '#49d1cc', '#636efb', '#90ef91', '#ef553b',
          '#ff8c02', '#07cc96', '#ac64fa', '#ffa25a', '#1ad3f3',
          '#ff98ff', '#fecb53', '#ff6792', '#ff98ff', '#c7cafd',
          '#e1c6fd', '#ffdbc1', '#b7e880', '#f7a79a', '#7ae6f9',
          '#ffccdb', '#e8f8d6', '#32ffc9', '#fffdff', '#ffe9b7',
          '#84d92b', '#ff0249', '#ff32ff', '#07899f', '#f36a02',
          '#00664b', '#7609ef', '#b5270f', '#0f19f0', '#cccccc',
          '#76ff77', '#77ddbb', '#aaaaff', '#ff88ff', '#fecc87',
          '#febc55', '#fe7777', '#ff3333', '#aa0000',
         ]

monthMap = {
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

divisionMap = {
    0: 'Others',
    1: 'Div1',
    2: 'Div2',
    3: 'Div3',
    4: 'Div4'
}

rankMapColor = {
    'newbie': '#cccccc',
    'pupil': '#76ff77',
    'specialist': '#77ddbb',
    'expert': '#aaaaff',
    'candidate master': '#ff88ff',
    'master': '#fecc87',
    'international master': '#febc55',
    'grandmaster': '#fe7777',
    'international grandmaster': '#ff3333',
    'legendary grandmaster': '#aa0000'
}

divisionMapColor = {
    'others': 'lightgreen',
    'div1': '#ff6792',
    'div2': 'gold',
    'div3': 'mediumturquoise',
    'div4': 'darkorange'
}

modeSolvedMapColor = {
    'CONTESTANT': 'gold',
    'PRACTICE': 'mediumturquoise',
    'VIRTUAL': 'darkorange',
    'OUT_OF_COMPETITION': 'lightgreen',
    'MANAGER': '#ff6792'
}

verdictMapColors = {
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

tagMapColor = {
    'implementation': 0,
    'math': 1,
    'greedy': 2,
    'dp': 3,
    'data structures': 4,
    'brute force': 5,
    'constructive algorithms': 6,
    'graphs': 7,
    'sortings': 8,
    'binary search': 9,
    'dfs and similar': 10,
    'trees': 11,
    'strings': 12,
    'number theory': 13,
    'combinatorics': 14,
    '*special': 15,
    'geometry': 16,
    'bitmasks': 17,
    'two pointers': 18,
    'dsu': 19,
    'shortest paths': 20,
    'probabilities': 21,
    'divide and conquer': 22,
    'hashing': 23,
    'games': 24,
    'flows': 25,
    'interactive': 26,
    'matrices': 27,
    'string suffix structures': 28,
    'fft': 29,
    'graph matchings': 30,
    'ternary search': 31,
    'expression parsing': 32,
    'meet-in-the-middle': 33,
    '2-sat': 34,
    'chinese remainder theorem': 35,
    'schedules': 36,
}