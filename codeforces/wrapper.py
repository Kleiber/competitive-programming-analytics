import utils

# Problems that the user solves
class Problem:
    id = ""
    contestId = ""
    letter = ""
    verdict = ""
    solvedType = ""
    rating = 0
    tags = []
    programmingLanguage = ""
    submissionDate = None

    def __init__(self, id, contestId, letter, verdict, solvedType, rating, tags, programmingLanguage, submissionDate):
        self.id = id
        self.contestId = contestId
        self.letter = letter
        self.verdict = verdict
        self.solvedType = solvedType
        self.rating = rating
        self.tags = tags
        self.programmingLanguage = programmingLanguage
        self.submissionDate = submissionDate

# Contests that the user participated
class Contest:
    id = ""
    division = ""
    rating = 0
    solvedProblems = 0
    date = None

    def __init__(self, id, division, rating, solvedProblems, date):
        self.id = id
        self.division = division
        self.rating = rating
        self.solvedProblems = solvedProblems
        self.date = date

# User information
class Info:
    handle = ""
    firstName = ""
    lastName = ""
    rating = 0
    maxRating = 0
    rank = ""
    maxRank = ""
    photo = ""
    registrationDate = None
    lastOnlineDate = None

    def __init__(self, handle, firstName, lastName, rating, maxRating, rank, maxRank, photo, registrationDate, lastOnlineDate):
        self.handle = handle
        self.firstName = firstName
        self.lastName = lastName
        self.rating = rating
        self.maxRating = maxRating
        self.rank = rank
        self.maxRank = maxRank
        self.photo = photo
        self.registrationDate = registrationDate
        self.lastOnlineDate = lastOnlineDate

# Complete information about the Codeforces user
class User:
    info = None
    contests = {}
    problems = {}

    def __init__(self, handle, yearFilter):
        self.getUserInfo(handle)
        self.getUserProblems(handle, yearFilter)
        self.getUserContests(handle, yearFilter)

    def getUserInfo(self, handle):
        link = f"https://codeforces.com/api/user.info?handles={handle}"
        data = utils.getDataFromRequest(link)

        if data['status'] != "OK":
            print("Error occurred: {}".format(data['comment']))
            return

        user = data['result'][0]
        firstName = utils.getMapValue(user, 'firstName', str)
        lastName = utils.getMapValue(user, 'lastName', str)
        rating = utils.getMapValue(user, 'rating', int)
        maxRating = utils.getMapValue(user, 'maxRating', int)
        rank = utils.getMapValue(user, 'rank', int)
        maxRank = utils.getMapValue(user, 'maxRank', int)
        titlePhoto = utils.getMapValue(user, 'titlePhoto', str)
        registrationDateSeconds= utils.getMapValue(user, 'registrationTimeSeconds', str)
        lastOnlineDateSeconds = utils.getMapValue(user, 'lastOnlineTimeSeconds', str)

        registrationDate = utils.getDate(registrationDateSeconds)
        lastOnlineDate = utils.getDate(lastOnlineDateSeconds)

        self.info = Info(handle, firstName, lastName, rating, maxRating, rank, maxRank, titlePhoto, registrationDate, lastOnlineDate)

    def getUserProblems(self, handle, yearFilter):
        if self.info == None:
            return

        link = f"https://codeforces.com/api/user.status?handle={handle}"
        data = utils.getDataFromRequest(link)

        if data['status'] != "OK":
            print("Error occurred: {}".format(data['comment']))
            return

        visited = {}
        submissions = data['result']
        for submission in submissions:
            problem = submission['problem']
            verdict = submission['verdict']
            author = submission['author']
            programmingLanguage = submission['programmingLanguage']
            creationTimeSeconds = submission['creationTimeSeconds']

            contestId = utils.getMapValue(problem, 'contestId', int)
            problemsetName = utils.getMapValue(problem, 'problemsetName', str)
            index = problem['index']
            rating = utils.getMapValue(problem, 'rating', int)
            tags = problem['tags']
            participantType = author['participantType']

            id = problemsetName + str(contestId) + index
            submissionDate = utils.getDate(creationTimeSeconds)

            if yearFilter != submissionDate.year and yearFilter != 0:
                continue

            if id in visited:
                if verdict == "OK": 
                    self.problems[id] = Problem(id, contestId, index, verdict, participantType, rating, tags, programmingLanguage, submissionDate)
            else:
                visited[id] = True
                self.problems[id] = Problem(id, contestId, index, verdict, participantType, rating, tags, programmingLanguage, submissionDate)

    def getUserContests(self, handle, yearFilter):
        if self.info == None:
            return
        if not self.problems:
            return

        link = f"https://codeforces.com/api/user.rating?handle={handle}"
        dataContest = utils.getDataFromRequest(link)

        if dataContest['status'] != "OK":
            print("Error occurred: {}".format(dataContest['comment']))
            return
        
        contests = dataContest['result']
        for contest in contests:
            id = contest['contestId']
            name = contest['contestName']
            oldRating = contest['oldRating']
            newRating = contest['newRating']
            contestDate = utils.getDate(contest['ratingUpdateTimeSeconds'])

            if yearFilter != contestDate.year and yearFilter != 0:
                continue

            rating = newRating - oldRating
    
            solvedProblems = 0
            for key in self.problems:
                if self.problems[key].contestId == id and self.problems[key].solvedType == "CONTESTANT" and self.problems[key].verdict == "OK":
                    solvedProblems += 1
                    
            division = utils.getDivision(0)
            if "div. 1" in name.lower():
                division = utils.getDivision(1)
            if "div. 2" in name.lower():
                division = utils.getDivision(2)
            if "div. 3" in name.lower():
                division = utils.getDivision(3)
            if "div. 4" in name.lower():
                division = utils.getDivision(4)

            self.contests[id] = Contest(id, division, rating, solvedProblems, contestDate)

def getUser(handle, yearFilter):
    print('Load data from Codeforces for \'{}\' user...'.format(handle))
    user = User(handle, yearFilter)
    return user
