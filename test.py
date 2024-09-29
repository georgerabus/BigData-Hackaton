import json

# Define the path to the JSON file
path1 = "./data/0a866589-0d5d-4a9f-9121-89530653f42c.json"

# Try to read and parse the JSON file
try:
    with open(path1, 'r') as file:
        file_contents = file.read()  # Read the content of the file
    
    # Load the JSON data
    data = json.loads(file_contents)  # Parse the JSON

    # Print the data to verify
    print(data)

except FileNotFoundError:
    print(f"Error: The file at {path1} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
