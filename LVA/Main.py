import csv
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from sklearn.metrics import precision_score, recall_score, accuracy_score
from tksheet import Sheet

class MatchmakingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Matchmaking App")
        self.master.geometry("1000x800")

        self.master.columnconfigure(0, weight=1)  # Column 0 (containing the sheet frames) will expand horizontally

        self.dataset_label = tk.Label(self.master, text="Dataset File:")
        self.dataset_label.grid(row=0, column=0)

        self.dataset_path = tk.StringVar()
        self.dataset_entry = tk.Entry(self.master, textvariable=self.dataset_path, width=50)
        self.dataset_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_dataset)
        self.browse_button.grid(row=0, column=2)

        self.run_button = tk.Button(self.master, text="Run Matchmaking", command=self.run_matchmaking)
        self.run_button.grid(row=0, column=3)

        self.team1_label = tk.Label(self.master, text="Team 1")
        self.team1_label.grid(row=1, column=0, pady=(10, 0))

        self.team2_label = tk.Label(self.master, text="Team 2")
        self.team2_label.grid(row=3, column=0, pady=(10, 0))

        self.sheet_frame_team1 = Sheet(self.master, headers=["nickname", "id", "country", "rating", "averageCombatScore", "roundsPlayed", "kdRatio", "kills", "deaths", "assists", "killsPerRound", "deathsPerRound", "assistsPerRound"])
        self.sheet_frame_team1.grid(row=2, column=0, sticky="nsew")  # Expanded horizontally and vertically

        self.sheet_frame_team2 = Sheet(self.master, headers=["nickname", "id", "country", "rating", "averageCombatScore", "roundsPlayed", "kdRatio", "kills", "deaths", "assists", "killsPerRound", "deathsPerRound", "assistsPerRound"])
        self.sheet_frame_team2.grid(row=4, column=0, sticky="nsew")  # Expanded horizontally and vertically

        self.precision_label = tk.Label(self.master, text="Precision:")
        self.precision_label.grid(row=5, column=0, sticky='e')

        self.recall_label = tk.Label(self.master, text="Recall:")
        self.recall_label.grid(row=6, column=0, sticky='e')

        self.accuracy_label = tk.Label(self.master, text="Accuracy:")
        self.accuracy_label.grid(row=7, column=0, sticky='e')

        self.precision_value = tk.StringVar()
        self.precision_output = tk.Label(self.master, textvariable=self.precision_value)
        self.precision_output.grid(row=5, column=1, sticky='w')

        self.recall_value = tk.StringVar()
        self.recall_output = tk.Label(self.master, textvariable=self.recall_value)
        self.recall_output.grid(row=6, column=1, sticky='w')

        self.accuracy_value = tk.StringVar()
        self.accuracy_output = tk.Label(self.master, textvariable=self.accuracy_value)
        self.accuracy_output.grid(row=7, column=1, sticky='w')

    def browse_dataset(self):
        filename = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if filename:
            self.dataset_path.set(filename)

    def read_csv(self, filename):
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

    def generate_teams(self, player):
        # Shuffle the player data randomly
        random.shuffle(player)

        # Split the shuffled player data into two teams
        team1 = player[:5]
        team2 = player[5:10]

        return team1, team2

    def print_teams(self, team, sheet_frame):
        data = [[player[field] for field in player] for player in team]
        sheet_frame.set_sheet_data(data)

    def calculate_metrics(self, labels, predictions):
        precision = precision_score(labels, predictions)
        recall = recall_score(labels, predictions)
        accuracy = accuracy_score(labels, predictions)

        return precision, recall, accuracy

    def run_matchmaking(self):
        filename = self.dataset_path.get()
        if not filename:
            messagebox.showerror("Error", "Please select a dataset file.")
            return

        player_data = self.read_csv(filename)
        team1, team2 = self.generate_teams(player_data)

        # Print teams
        self.print_teams(team1, self.sheet_frame_team1)
        self.print_teams(team2, self.sheet_frame_team2)

        # Extract labels for evaluation (1 for team 1, 0 for team 2)
        labels = [1] * 5 + [0] * 5

        # Example: Randomly assign labels as predictions
        predictions = [random.choice([0, 1]) for _ in range(10)]

        # Calculate precision, recall, and accuracy
        precision, recall, accuracy = self.calculate_metrics(labels, predictions)

        # Display metrics
        self.precision_value.set(f"{precision:.2f}")
        self.recall_value.set(f"{recall:.2f}")
        self.accuracy_value.set(f"{accuracy:.2f}")

def main():
    root = tk.Tk()
    app = MatchmakingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
