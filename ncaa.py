import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def score(team1, team2):
    team1 = form(team1)
    team2 = form(team2)
    result = []
    req = requests.get(f"https://data.ncaa.com/casablanca/game/basketball-men/d1/{datetime.now().year}/" +
                       f"{datetime.now().strftime('%m')}/{datetime.now().strftime('%d')}/{team1}-{team2}/gameInfo.json")
    file = json.loads(req.text)
    result.append(float(file["away"]["score"]) + float(file["home"]["score"]))
    result.append(float(file["away"]["score"]))
    result.append(float(file["home"]["score"]))
    return result


def time(team1, team2):
    team1 = form(team1)
    team2 = form(team2)
    req = requests.get(f"https://data.ncaa.com/casablanca/game/basketball-men/d1/{datetime.now().year}/" +
                       f"{datetime.now().strftime('%m')}/{datetime.now().strftime('%d')}/{team1}-{team2}/gameInfo.json")
    file = json.loads(req.text)
    if file["status"]["currentPeriod"][0] is not 'H':
        remain_time = float(file["status"]["clock"].split(':')[0]) + float(file["status"]["clock"].
                                                                           split(':')[1]) / 60
        half = float(file["status"]["currentPeriod"][0])
    else:
        remain_time = 0
        half = 1
    result = (2 - half) * 20 + remain_time

    return result


def poss(team1, team2):
    team1 = form(team1)
    team2 = form(team2)
    req = requests.get(f"https://data.ncaa.com/casablanca/game/basketball-men/d1/{datetime.now().year}/" +
                       f"{datetime.now().strftime('%m')}/{datetime.now().strftime('%d')}/{team1}-{team2}/boxscore.json")
    file = json.loads(req.text)
    tFGA = float(file["teams"][0]["playerTotals"]["fieldGoalsMade"].split('-')[1])
    tFTA = float(file["teams"][0]["playerTotals"]["freeThrowsMade"].split('-')[1])
    tORB = float(file["teams"][0]["playerTotals"]["offensiveRebounds"])
    tDRB = float(file["teams"][0]["playerTotals"]["totalRebounds"]) - tORB
    tFG = float(file["teams"][0]["playerTotals"]["fieldGoalsMade"].split('-')[0])
    tTO = float(file["teams"][0]["playerTotals"]["turnovers"])
    oFGA = float(file["teams"][1]["playerTotals"]["fieldGoalsMade"].split('-')[1])
    oFTA = float(file["teams"][1]["playerTotals"]["freeThrowsMade"].split('-')[1])
    oORB = float(file["teams"][1]["playerTotals"]["offensiveRebounds"])
    oDRB = float(file["teams"][1]["playerTotals"]["totalRebounds"]) - oORB
    oFG = float(file["teams"][1]["playerTotals"]["fieldGoalsMade"].split('-')[0])
    oTO = float(file["teams"][1]["playerTotals"]["turnovers"])

    result = 0.5 * ((tFGA + 0.4 * tFTA - 1.07 * (tORB / (tORB + oDRB)) * (tFGA - tFG) + tTO)
                    + (oFGA + 0.4 * oFTA - 1.07 * (oORB / (oORB + tDRB)) * (oFGA - oFG) + oTO))

    return result


def ortg(team1, team2):
    result = []
    replace_dict = {'State': 'St.', ' ': '+', '&': '%26', 'Lsu': 'LSU', 'Johns': 'John%27s', 'Tcu': 'TCU',
                    'Nc': 'North+Carolina', 'Usc': 'USC', 'Ucla': 'UCLA'}
    req = requests.get("https://kenpom.com/index.php").text
    soup = BeautifulSoup(req, 'lxml')
    team1 = team1.lower().title()
    team2 = team2.lower().title()
    for old, new in replace_dict:
        team1 = team1.replace(old, new)
        team2 = team2.replace(old, new)
    row1 = soup.find(href="team.php?team=" + team1)
    rating1 = row1.parent.next_sibling.next_sibling.next_sibling.next_sibling.string
    row2 = soup.find(href="team.php?team=" + team2)
    rating2 = row2.parent.next_sibling.next_sibling.next_sibling.next_sibling.string
    result.append(float(rating1) / 100)
    result.append(float(rating2) / 100)
    return result


def form(team1):
    replace_dict = {' ': '-', 'state': 'st', 'st.-johns': 'st-johns-ny', 'kentucky-': 'ky-', 'georgia-': 'ga-',
                    'nc-': 'north-carolina-', '-florida': '-fla', '&': '', '.': '', 'connecticut': 'uconn',
                    '-chicago': '-il', '-illinois': 'ill', 'mississippi': 'ole-miss', 'ga-tech': 'georgia-tech',
                    'usc': 'southern-california'}
    team = team1.lower()
    for old, new in replace_dict:
        team = team.replace(old, new)
    return team
