# Create a file named app.py
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import pytz
from config import DAILY_TASKS, create_default_daily_tasks_object

app = Flask(__name__)

pacific_timezone = pytz.timezone('US/Pacific')

@app.route('/')
def hello():
    file_name = get_todo_filename()
    file_data = make_or_get_file(file_name)
    return render_template('todo.html', data=file_data)

def get_todo_filename():
    current_date = get_current_date()

    # Check if it's time to create a new file
    if after_date_cutoff():
        return f"todo_list_{current_date}.json"
    else:
        # Use the previous day's date for the filename
        previous_day = current_datetime - timedelta(days=1)
        return f"todo_list_{previous_day.strftime('%Y-%m-%d')}.json"

def get_current_date():
    # Get the current date in the desired time zone (PST)
    current_datetime = datetime.now(pacific_timezone)
    return current_datetime.strftime("%Y-%m-%d")

def after_date_cutoff():
    # Get the current time in the desired time zone (PST)
    current_datetime = datetime.now(pacific_timezone)

    # Define the switch-over time (2 AM PST)
    switch_over_time = current_datetime.replace(hour=2, minute=0, second=0, microsecond=0)

    # Check if the current time is after the switch-over time
    return current_datetime >= switch_over_time

def make_or_get_file(file_name):
    # Check if the data file exists
    if os.path.exists(file_name):
        # If the file exists, read its content
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        default_data = create_default_daily_tasks_object()
        # Create the file and write default data
        with open(file_name, 'w') as file:
            json.dump(default_data, file, indent=4)
        return default_data

@app.route('/data', methods=['POST'])
def data():
    try:
        data = request.get_json()
        if not authenticate_request(data):
            return jsonify({"error": "Unauthorized"}), 403

        # Get the field to update and its new value from the request
        field_name = data.get('elementId')
        new_value = data.get('newValue')

        if isinstance(field_name, str):
            field_info = DAILY_TASKS.get(field_name)
        else:
            return jsonify({"error": "Field name to update is required."}), 400

        if field_info:
            data_type = field_info.get('data_type')
        else:
            data_type = None

        # Ensure the field name is correct
        if data_type is None:
            return jsonify({"error": "Invalid field name."}), 400

        # Ensure the value is the correct type.
        try:
            # Attempt to convert the input value to the expected data type
            new_value = data_type(new_value)
            
            if data_type == str and len(new_value) > 200:
                return jsonify({"error": f'String value for field {field_name} is too long (max 200 characters).'}), 400
        except (ValueError, TypeError):
            # Handle the case where conversion is not possible
            return jsonify({"error": f'Invalid value for the field: {field_name}'}), 400

        file_name = get_todo_filename()

        # Read the existing data from the JSON file
        existing_data = make_or_get_file(file_name)

        existing_data[field_name] = new_value

        # Save the updated data back to the JSON file
        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)

        return jsonify({"message": "Field updated successfully."}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

def authenticate_request(data):
    return data.get('password') == "temp"

if __name__ == '__main__':
    app.run()
