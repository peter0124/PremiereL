import networkx as nx
import csv
import datetime
from colorama import Fore, Style
graph = nx.DiGraph()
team_results = {}
choice = input("Calculate table by (1) date or (2) round? ")
if choice == "1":
    target_date = input("Enter target date (DD-MM-YYYY): ")
    target_date = datetime.datetime.strptime(target_date, "%d-%m-%Y")
    with open("matches.csv") as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            round, date, home_team, away_team, score1, score2, result = row
            match_date = datetime.datetime.strptime(date, "%d/%m/%Y")
            # converting it to a datetime object that you can then compare to the target date input by the user.
            if result == '-':
                continue
            if match_date <= target_date:
                if score1 > score2:
                    home_points = 3
                elif score1 < score2:
                    home_points = 0
                else:
                    home_points = 1
                graph.add_node(home_team)
                graph.add_node(away_team)
                graph.add_edge( home_team, away_team, weight=home_points, score1 = score1, score2 = score2)
elif choice == "2":
    target_round = int(input("Enter target round number: "))
    with open("matches.csv") as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            round, date, home_team, away_team, score1, score2, result = row
            if result == '-':
                continue
            if  int(round) <= target_round:
                if score1 > score2:
                    home_points = 3
                elif score1 < score2:
                    home_points = 0
                else:
                    home_points = 1
                graph.add_node(home_team)
                graph.add_node(away_team)
                graph.add_edge( home_team, away_team, weight=home_points, score1 = score1, score2 = score2)

def count(team):
    goals_scored = 0
    goals_conceded = 0 
    wins = 0
    losses = 0
    draws = 0
    if team in team_results:
        return team_results[team]
    for u,v,data in graph.edges(data=True):
        if u == team:
            goals_scored += int(data.get('score1', 0))
            goals_conceded += int(data.get('score2', 0))
            if data['weight'] == 3:
                wins += 1
            elif data['weight'] == 0:
                losses += 1
            elif data['weight'] == 1:
                draws += 1
        if v == team:
            goals_scored += int(data.get('score2', 0))
            goals_conceded += int(data.get('score1', 0))
            if data['weight'] == 0:
                wins += 1
            elif data['weight'] == 3:
                losses += 1
            elif data['weight'] == 1:
                draws += 1
        team_results[team] = { "wins": wins, "losses": losses, "draws": draws, "goals_scored": goals_scored, "goals_conceded": goals_conceded}
    return team_results[team]

standings = [(count(team)["wins"], team ) for team in graph.nodes()]
standings = []
for team in graph.nodes():
    result = team_results[team]
    points = result["wins"]*3 + result["draws"]
    goals_scored = result["goals_scored"]
    goals_conceded = result["goals_conceded"]
    losses = result["losses"]
    wins = result["wins"]
    draws = result["draws"]
    standings.append((points, team, goals_scored, goals_conceded, wins, losses, draws))

standings = sorted(standings, key=lambda x: (x[0], x[2] - x[3], x[4]), reverse=True)
print(Style.BRIGHT + f"\033[3mPos Team                               M      P      W      D      L     GS     GC     GD\033[0m")
print("-" * 89)
for pos, (points, team, goals_scored, goals_conceded, wins, losses, draws) in enumerate(standings, start=1):
    color = (Fore.BLUE if pos < 5 else
            Fore.GREEN if pos == 5 else
            Fore.RED if pos > 17 else
            ""  )
    print(Style.BRIGHT + color + f"\033[3m{pos:2} {team:<30}  {(wins + draws + losses):5}  {points:5}  {wins:5}  {draws:5}  {losses:5}  {goals_scored:5}  {goals_conceded:5}  {goals_scored - goals_conceded:5}\033[0m" + Style.RESET_ALL)
print("-" * 89)