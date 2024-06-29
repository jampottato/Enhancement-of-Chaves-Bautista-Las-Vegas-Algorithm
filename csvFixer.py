import csv

def fix_utf8_error(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        # Read the CSV file
        reader = csv.reader(f)
        data = [row for row in reader]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Write the fixed data into a new CSV file
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == "__main__":
    input_file = './Dataset/ValorantPlayerPoolStats.csv'  # Change this to the path of your input CSV file
    output_file = './Dataset/fixed_output.csv'  # Change this to the desired name of the output fixed CSV file
    fix_utf8_error(input_file, output_file)
    print("Fixed CSV file saved as:", output_file)
