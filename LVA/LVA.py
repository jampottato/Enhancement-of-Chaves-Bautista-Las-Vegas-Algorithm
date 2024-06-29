import csv
import random
import time
from prettytable import PrettyTable


def read_csv(filename):
    data = []
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']  # Add more encodings if necessary

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            break  # If successful, exit the loop
        except UnicodeDecodeError:
            continue  # If decoding fails, try the next encoding

    return data


def generate_teams(player):
    # Shuffle the player data randomly
    random.shuffle(player)

    # Split the shuffled player data into two teams
    team1 = player[:5]
    team2 = player[5:10]

    return team1, team2

def print_teams(team1, team2):
    headers = ["nickname", "id", "country", "rating", "averageCombatScore", "roundsPlayed", "kdRatio", "kills", "deaths", "assists", "killsPerRound", "deathsPerRound", "assistsPerRound"]

    print("Team 1:")
    table1 = PrettyTable(headers)
    for player in team1:
        row_data = [player[header] for header in headers]
        table1.add_row(row_data)
    print(table1)

    print("\nTeam 2:")
    table2 = PrettyTable(headers)
    for player in team2:
        row_data = [player[header] for header in headers]
        table2.add_row(row_data)
    print(table2)


if __name__ == "__main__":
    start_time = time.time()

    # Read data from CSV file
    filename = './Dataset/ValorantPlayerPoolStats.csv'
    player_data = read_csv(filename)

    # Generate teams
    team1, team2 = generate_teams(player_data)

    # Print teams
    print_teams(team1, team2)

    end_time = time.time()
    runtime = end_time - start_time
    minutes = int(runtime // 60)
    seconds = int(runtime % 60)
    milliseconds = int((runtime - int(runtime)) * 1000)
    print("\nTotal runtime:", f"{minutes} minutes, {seconds} seconds, {milliseconds} milliseconds")
