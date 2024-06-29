import tkinter as tk
from tkinter import filedialog
import json
import csv
import os

class JSONDataExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Data Extractor")
        
        # UI elements
        self.file_label = tk.Label(root, text="Select JSON file:")
        self.file_label.pack()
        
        self.file_button = tk.Button(root, text="Browse", command=self.browse_json_file)
        self.file_button.pack()
        
        self.columns_label = tk.Label(root, text="Enter column headers (comma-separated):")
        self.columns_label.pack()
        
        self.columns_entry = tk.Entry(root)
        self.columns_entry.pack()
        
        self.add_header_button = tk.Button(root, text="Add Header", command=self.add_header_entry)
        self.add_header_button.pack()
        
        self.extract_button = tk.Button(root, text="Extract Data", command=self.extract_data)
        self.extract_button.pack()
        
        self.header_entries = []  # To store entry widgets for column headers
        
    def browse_json_file(self):
        self.json_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        print("Selected JSON file:", self.json_file_path)
        
    def add_header_entry(self):
        header_entry = tk.Entry(self.root)
        header_entry.pack()
        self.header_entries.append(header_entry)
        
    def extract_data(self):
        if not hasattr(self, 'json_file_path'):
            print("Please select a JSON file.")
            return
        
        column_headers = [self.columns_entry.get()]  # Getting the first entry
        column_headers.extend(entry.get() for entry in self.header_entries)  # Getting the rest of the entries
        
        print("Column Headers:", column_headers)
        
        with open(self.json_file_path) as f:
            data = json.load(f)
            
        # Extract data based on user input
        extracted_data = []
        self.extract_data_recursive(data, column_headers, extracted_data)
        
        # Save extracted data as CSV
        self.save_as_csv(extracted_data, column_headers)
        
        print("Data extracted and saved successfully.")
        
    def extract_data_recursive(self, data, column_headers, extracted_data, parent_key=''):
        if isinstance(data, dict):
            # Check if all column headers are present in current data
            if all(header in data for header in column_headers):
                row = {header: data[header] for header in column_headers}
                extracted_data.append(row)
            for key, value in data.items():
                new_key = f"{parent_key}_{key}" if parent_key else key
                if isinstance(value, (dict, list)):
                    self.extract_data_recursive(value, column_headers, extracted_data, new_key)
        elif isinstance(data, list):
            for item in data:
                self.extract_data_recursive(item, column_headers, extracted_data, parent_key)
        
    def save_as_csv(self, data, column_headers):
        csv_filename = os.path.join("Dataset", "southeast asia extracted.csv")
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)
            writer.writeheader()
            writer.writerows(data)

            def get_subdata(self, data):
                if isinstance(data, dict):
                    subdata = data.get("team")
                    if subdata:
                        subdata_id = subdata.get("id")
                        subdata_title = subdata.get("title")
                        return subdata_id, subdata_title
                return None, None


# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = JSONDataExtractor(root)
    root.mainloop()
