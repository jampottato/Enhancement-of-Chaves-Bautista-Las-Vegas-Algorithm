import tkinter as tk
from tkinter import scrolledtext
import csv
import random
import time
from prettytable import PrettyTable
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

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

    output_text = ""
    output_text += "Team 1:\n"
    table1 = PrettyTable(headers)
    for player in team1:
        row_data = [player[header] for header in headers]
        table1.add_row(row_data)
    output_text += str(table1) + "\n"

    output_text += "\nTeam 2:\n"
    table2 = PrettyTable(headers)
    for player in team2:
        row_data = [player[header] for header in headers]
        table2.add_row(row_data)
    output_text += str(table2) + "\n"

    return output_text

def calculate_metrics(labels, predictions):
    precision = precision_score(labels, predictions)
    recall = recall_score(labels, predictions)
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions)
    return precision, recall, accuracy, f1

def run_iterations(total_iterations, player_data):
    output_text = ""
    runtimes = []
    for i in range(total_iterations):
        start_time = time.time()

        # Generate teams
        team1, team2 = generate_teams(player_data)

        # Print teams
        output_text += f"\nIteration {i + 1}/{total_iterations}:\n"
        output_text += print_teams(team1, team2)

        # Extract labels for evaluation (1 for team 1, 0 for team 2)
        labels = [1] * 5 + [0] * 5

        # Example: Randomly assign labels as predictions
        predictions = [random.choice([0, 1]) for _ in range(10)]

        # Calculate metrics
        precision, recall, accuracy, f1 = calculate_metrics(labels, predictions)

        output_text += "\nPrecision: {}\n".format(precision)
        output_text += "Recall: {}\n".format(recall)
        output_text += "Accuracy: {}\n".format(accuracy)
        output_text += "F1 Score: {}\n".format(f1)

        end_time = time.time()
        runtime = end_time - start_time
        runtimes.append(runtime)
        seconds = int(runtime)
        milliseconds = int((runtime - seconds) * 1000)
        output_text += "Runtime: {} seconds {} milliseconds\n".format(seconds, milliseconds)

    average_runtime = sum(runtimes) / len(runtimes)
    seconds = int(average_runtime)
    milliseconds = int((average_runtime - seconds) * 1000)
    output_text += "\nAverage iteration runtime: {} seconds {} milliseconds\n".format(seconds, milliseconds)

    return output_text

if __name__ == "__main__":
    # Read data from CSV file
    filename = './Dataset/ValorantPlayerPoolStats.csv'
    player_data = read_csv(filename)

    # Create Tkinter window
    root = tk.Tk()
    root.title("Iteration Results")

    # Create a scrolled text widget
    output_text = scrolledtext.ScrolledText(root, width=100, height=30)
    output_text.pack(expand=True, fill="both")

    # Run iterations and display results
    output_text.insert(tk.END, run_iterations(100, player_data))

    root.mainloop()
