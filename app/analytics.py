import sys
import plotly.express as px
import plotly.graph_objects as go

import wrapper
import utils

class Analytics:
    def __init__(self, user):
        self.statusContest = {}
        self.topicContest = {}
        self.divisionContest = {}

        self.statusProblem = {}
        self.topicProblem = {}
        self.ratingProblem = {}
        self.modeSolvedProblem = {}

        self.countContestByDivision = {}

        self.contestProblemByStatus = {}
        self.contestProblemByTag = {}
        self.contestByDivision = {}
        self.contestMonthRating = {}

        self.problemByStatus = {}
        self.problemByTag = {}
        self.problemByMode = {}
        self.problemByRating = {}

        self.minMonthSubmission = 2030
        self.maxMonthSubmission = 0
        self.minYearSubmission = 2030
        self.maxYearSubmission = 0

        self.user = user
        self.Initialization()

    def Initialization(self):
        # Contests
        for key in self.user.contests:
            contest = self.user.contests[key]

            # Solved contest problems by divisions
            if contest.division not in self.divisionContest:
                self.divisionContest[contest.division] = 0
            self.divisionContest[contest.division] += contest.solvedProblems

            if contest.division not in self.countContestByDivision:
                self.countContestByDivision[contest.division] = 0
            self.countContestByDivision[contest.division] += 1

            if contest.division not in self.contestByDivision:
                self.contestByDivision[contest.division] = []
            self.contestByDivision[contest.division].append(contest)

            if contest.date.month not in self.contestMonthRating:
                self.contestMonthRating[contest.date.month] = []
            self.contestMonthRating[contest.date.month].append(contest)

        # Problems
        for key in self.user.problems:
            problem = self.user.problems[key]

            # Problem submission
            if problem.verdict not in self.statusProblem:
                self.statusProblem[problem.verdict] = 0
            self.statusProblem[problem.verdict] += 1

            if problem.verdict not in self.problemByStatus:
                self.problemByStatus[problem.verdict] = []
            self.problemByStatus[problem.verdict].append(problem)

            # Problem solved
            if problem.verdict == "OK":
                if problem.solvedType not in self.modeSolvedProblem:
                    self.modeSolvedProblem[problem.solvedType] = 0
                self.modeSolvedProblem[problem.solvedType] += 1

                for tag in problem.tags:
                    if tag not in self.topicProblem:
                        self.topicProblem[tag] = 0
                    self.topicProblem[tag] += 1

                    if tag not in self.problemByTag:
                        self.problemByTag[tag] = []
                    self.problemByTag[tag].append(problem)

                if problem.rating not in self.ratingProblem:
                    self.ratingProblem[problem.rating] = 0
                self.ratingProblem[problem.rating] += 1

                if problem.rating not in self.problemByRating:
                    self.problemByRating[problem.rating] = []
                self.problemByRating[problem.rating].append(problem)

                if problem.solvedType not in self.problemByMode:
                    self.problemByMode[problem.solvedType] = []
                self.problemByMode[problem.solvedType].append(problem)

            # Problem submission in contest
            if problem.solvedType == "CONTESTANT":
                if problem.verdict not in self.statusContest:
                    self.statusContest[problem.verdict] = 0
                self.statusContest[problem.verdict] += 1

                if problem.verdict not in self.contestProblemByStatus:
                    self.contestProblemByStatus[problem.verdict] = []
                self.contestProblemByStatus[problem.verdict].append(problem)

            # Solved problem in contest
            if problem.solvedType == "CONTESTANT" and problem.verdict == "OK":
                for tag in problem.tags:
                    if tag not in self.topicContest:
                        self.topicContest[tag] = 0
                    self.topicContest[tag] += 1

                    if tag not in self.contestProblemByTag:
                        self.contestProblemByTag[tag] = []
                    self.contestProblemByTag[tag].append(problem)

    def getYearOrMonthFormat(self, mapByYearOrMonth, year):
        labels = []
        values = []

        # Format by year
        if year == 0:
            for year in range(self.minYearSubmission, self.maxYearSubmission + 1):
                labels.append(year)
                if year not in mapByYearOrMonth:
                    values.append(0)
                else:
                     values.append(mapByYearOrMonth[year])
        # Format by month
        else:
            for month in range(self.minMonthSubmission, self.maxMonthSubmission + 1):
                labels.append(utils.getMonth(month))
                if month not in mapByYearOrMonth:
                    values.append(0)
                else:
                    values.append(mapByYearOrMonth[month])

        return labels, values

    ######## CONTESTS ########

    def getCountContestByDivisionGraph(self):
        labels = list(self.countContestByDivision.keys())
        values = list(self.countContestByDivision.values())

        df = dict(participate=values, category=labels)
        color = utils.getRankColor(self.user.info.rank)

        fig = px.line_polar(df, r='participate', theta='category', line_close=True, template="ggplot2", color_discrete_sequence=[color], markers=True)
        fig.update_traces(fill='toself', textposition='top center')
        fig.update_layout(paper_bgcolor='#222222', polar=dict(bgcolor='#222222', angularaxis=dict(showticklabels=True, ticks=''), radialaxis=dict(showticklabels=False, ticks='')), font=dict(color='white', size=20))

        return fig

    def getStatusContestGraph(self):
        labels = list(self.statusContest.keys())
        values = list(self.statusContest.values())

        colors = []
        for verdict in labels:
            colors.append(utils.getVerdictColor(verdict))

        chart = go.Pie(labels=labels, values=values, hole=.5, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.75), title_text='Statuses Problems')
        fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))

        return fig

    def getDivisionContestGraph(self):
        labels = list(self.divisionContest.keys())
        values = list(self.divisionContest.values())

        colors = []
        for division in labels:
            colors.append(utils.getDivisionColor(division))

        chart = go.Pie(labels=labels, values=values, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.75), title_text='Division Solved Problems')
        fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))

        return fig

    def getTopicContestGraph(self):
        labels = list(self.topicContest.keys())
        values = list(self.topicContest.values())
        parents = [''] * len(labels)

        colors = []
        for tag in self.topicContest:
            colors.append(utils.getTagColor(tag))

        chart = go.Treemap(labels = labels, values = values, parents = parents, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='middle center')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', title_text='Topic Solved Problems')
        fig.update_traces(hoverinfo='label', marker=dict(colors=colors, line=dict(color='#000000', width=1)))

        return fig

    def getRatingContestGraph(self, year):
        ratingContest = []
        idsContest = []
        isFirst = True
        for key in self.user.contests:
            contest = self.user.contests[key]
            if isFirst and year == 0:
                isFirst = False
                continue
            ratingContest.append(contest.rating)
            idsContest.append('Contest ' + str(contest.id))

        labels = idsContest
        values = ratingContest

        chart = go.Bar(x=labels, y=values, marker=dict(cornerradius="30%"))
        fig = go.Figure(data=[chart])
        fig.update_layout(plot_bgcolor='#303030', xaxis={'visible': False, 'showticklabels': False}, title_text='Rating Earning')
        fig.update_traces(marker=dict(color='gold', line=dict(color='#000000', width=1)))

        return fig

    ######## CONTEST PROGRESS ########

    def getStatusContestProgressGraph(self, year):
        fig = go.Figure()

        for status in self.contestProblemByStatus:
            problemsByKey = {}
            for problem in self.contestProblemByStatus[status]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)

                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)

            chart = go.Bar(x=labels, y=values, name=status,  marker_color=utils.getVerdictColor(status), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Statuses Problems Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getDivisionContestProgressGraph(self, year):
        fig = go.Figure()

        for division in self.contestByDivision:
            contestByKey = {}
            for contest in self.contestByDivision[division]:
                key = contest.date.year
                if year != 0:
                    key =  contest.date.month

                    self.minMonthSubmission = min(self.minMonthSubmission, contest.date.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, contest.date.month)

                self.minYearSubmission = min(self.minYearSubmission, contest.date.year)
                self.maxYearSubmission = max(self.maxYearSubmission, contest.date.year)

                if key not in contestByKey:
                    contestByKey[key] = 0
                contestByKey[key] += contest.solvedProblems

            keys = list(contestByKey.keys())
            keys.sort()
            sortedContestByKey= {i: contestByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedContestByKey, year)

            chart = go.Bar(x=labels, y=values, name=division,  marker_color=utils.getDivisionColor(division), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Division Solved Problems Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getTagContestProgressGraph(self, year):
        fig = go.Figure()

        for tag in self.contestProblemByTag:
            problemsByKey = {}
            for problem in self.contestProblemByTag[tag]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)

                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)

            chart = go.Bar(x=labels, y=values, name=tag,  marker_color=utils.getTagColor(tag), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Topic Solved Problems Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getRatingContestProgressGraph(self, year):
        contestsByKey = {}
        for month in self.contestMonthRating:
            for contest in self.contestMonthRating[month]:
                key = contest.date.year
                if year != 0:
                    key =  contest.date.month

                    self.minMonthSubmission = min(self.minMonthSubmission, contest.date.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, contest.date.month)

                self.minYearSubmission = min(self.minYearSubmission, contest.date.year)
                self.maxYearSubmission = max(self.maxYearSubmission, contest.date.year)

                if key not in contestsByKey:
                    contestsByKey[key] = 0
                contestsByKey[key] += contest.rating

        keys = list(contestsByKey.keys())
        keys.sort()
        sortedContestsByKey= {i: contestsByKey[i] for i in keys}

        labels, values = self.getYearOrMonthFormat(sortedContestsByKey, year)

        chart = go.Bar(x=labels, y=values, marker=dict(cornerradius="30%"))
        fig = go.Figure(data=[chart])
        fig.update_layout(plot_bgcolor='#303030', title_text='Rating Earning Progress')
        fig.update_traces(marker=dict(color ='gold', line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    ######## PROBLEMS ########

    def getStatusProblemGraph(self):
        labels = list(self.statusProblem.keys())
        values = list(self.statusProblem.values())

        colors = []
        for verdict in labels:
            colors.append(utils.getVerdictColor(verdict))

        chart = go.Pie(labels=labels, values=values, hole=.5, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.75), title_text='Statuses')
        fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))

        return fig

    def getSolvedTypeProblemGraph(self):
        labels = list(self.modeSolvedProblem.keys())
        values = list(self.modeSolvedProblem.values())

        colors = []
        for mode in labels:
            colors.append(utils.getSolvedTypeColor(mode))

        chart = go.Pie(labels=labels, values=values, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.75), title_text='Solved Mode')
        fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))

        return fig

    def getTopicProblemGraph(self):
        labels = list(self.topicProblem.keys())
        values = list(self.topicProblem.values())
        parents = [''] * len(labels)

        colors = []
        for tag in self.topicProblem:
            colors.append(utils.getTagColor(tag))

        chart = go.Treemap(labels = labels, values = values, parents = parents, textinfo='value')
        fig = go.Figure(data=[chart])
        fig.update_traces(textposition='middle center')
        fig.update_layout(uniformtext_minsize=25, uniformtext_mode='hide', showlegend=True, title_text='Topic Solved')
        fig.update_traces(hoverinfo='label', marker=dict(colors=colors, line=dict(color='#000000', width=1)))

        return fig

    def getRatingProblemGraph(self):
        ratingColors = utils.getRatingColors()
        colors = []

        keys = list(self.ratingProblem.keys())
        keys.sort()
        sortedRatingProblem = {i: self.ratingProblem[i] for i in keys}

        labels = []
        for key in sortedRatingProblem.keys():
            labels.append("Rating " + str(key))
            colors.append(ratingColors[key])
        values = list(sortedRatingProblem.values())

        chart = go.Bar(x=labels, y=values, marker_color=colors)
        fig = go.Figure(data=[chart])
        fig.update_layout(plot_bgcolor='#303030', xaxis={'visible': False, 'showticklabels': False}, title_text='Rating Solved')
        fig.update_traces(marker=dict(line=dict(color='#000000', width=1), cornerradius="30%"))

        return fig

    ######## PROBLEMS PROGRESS ########

    def getStatusProblemProgressGraph(self, year):
        fig = go.Figure()

        for status in self.problemByStatus:
            problemsByKey = {}
            for problem in self.problemByStatus[status]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)

                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)   

            chart = go.Bar(x=labels, y=values, name=status,  marker_color=utils.getVerdictColor(status), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Statuses Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getSolvedModetProblemProgressGraph(self, year):
        fig = go.Figure()

        for mode in self.problemByMode:
            problemsByKey = {}
            for problem in self.problemByMode[mode]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)

                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)

            chart = go.Bar(x=labels, y=values, name=mode,  marker_color=utils.getSolvedTypeColor(mode), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Solved Mode Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getTagProblemProgressGraph(self, year):
        fig = go.Figure()

        for tag in self.problemByTag:
            problemsByKey = {}
            for problem in self.problemByTag[tag]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)

                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)

            chart = go.Bar(x=labels, y=values, name=tag,  marker_color=utils.getTagColor(tag), marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Topic Solved Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)

        return fig

    def getRatingProblemProgressGraph(self, year):
        ratingColors = utils.getRatingColors()

        fig = go.Figure()

        problemByRatingKeys = list(self.problemByRating.keys())
        problemByRatingKeys.sort()
        problemByRatingSorted= {i: self.problemByRating[i] for i in problemByRatingKeys}

        for rating in problemByRatingSorted:
            problemsByKey = {}
            for problem in problemByRatingSorted[rating]:
                key = problem.submissionDate.year
                if year != 0:
                    key =  problem.submissionDate.month

                    self.minMonthSubmission = min(self.minMonthSubmission, problem.submissionDate.month)
                    self.maxMonthSubmission = max(self.maxMonthSubmission, problem.submissionDate.month)

                self.minYearSubmission = min(self.minYearSubmission, problem.submissionDate.year)
                self.maxYearSubmission = max(self.maxYearSubmission, problem.submissionDate.year)
 
                if key not in problemsByKey:
                    problemsByKey[key] = 0
                problemsByKey[key] += 1

            keys = list(problemsByKey.keys())
            keys.sort()
            sortedProblemsByKey= {i: problemsByKey[i] for i in keys}

            labels, values = self.getYearOrMonthFormat(sortedProblemsByKey, year)

            chart = go.Bar(x=labels, y=values, name=rating,  marker_color=ratingColors[rating], marker=dict(cornerradius="30%"))
            fig.add_trace(chart)
            fig.update_layout(plot_bgcolor='#303030', title_text='Rating Solved Progress')
            fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))

        fig.update_layout(barmode='group', xaxis_tickangle=-45)        

        return fig
