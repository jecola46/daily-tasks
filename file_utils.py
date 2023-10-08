import os
import json

# Reads in the given file, if it does not exist, creates it with the default data callback given.
def get_or_generate_file(file_name, default_data_callback):
    # Check if the data file exists
    if os.path.exists(file_name):
        # If the file exists, read its content
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        default_data = default_data_callback()
        # Create the file and write default data
        with open(file_name, 'w') as file:
            json.dump(default_data, file, indent=4)
        return default_data
    
def write_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)