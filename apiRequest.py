import tkinter as tk
import requests
import json
import os

# Create URL label and entry


def fetch_and_save_data():
    url = url_entry.get()
    json_file_name = json_file_entry.get()

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors

        data = response.json()

        directory = "JsonData"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, json_file_name + ".json")
        with open(file_path, "w") as file:
            json.dump(data, file)

        status_label.config(text="Data saved successfully!")
    except requests.exceptions.RequestException as e:
        status_label.config(text="Error: Failed to fetch data!")
    except json.JSONDecodeError:
        status_label.config(text="Error: Invalid JSON response!")
    except requests.exceptions.HTTPError as e:
        status_label.config(text="Error: " + str(e))

# Create the main window
window = tk.Tk()
window.title("API Data Fetcher")
window.geometry("400x200")  # Set the size of the main window

# Create URL label and entry
url_label = tk.Label(window, text="API URL:")
url_label.pack(pady=(10, 0))
url_entry = tk.Entry(window)
url_entry.pack(padx=10, pady=5)

# Create JSON file name label and entry
json_file_label = tk.Label(window, text="JSON File Name:")
json_file_label.pack(pady=(10, 0))
json_file_entry = tk.Entry(window)
json_file_entry.pack(padx=10, pady=5)

# Create fetch button
fetch_button = tk.Button(window, text="Fetch and Save", command=fetch_and_save_data)
fetch_button.pack(pady=10)

# Create status label
status_label = tk.Label(window, text="")
status_label.pack(pady=(0, 10))

# Start the main loop
window.mainloop()
