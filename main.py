# Create a file named app.py
from flask import Flask, render_template, request, jsonify
from config import DAILY_TASKS, create_default_daily_tasks_object
from file_utils import get_or_generate_file, write_file
from time_utils import get_filename_for_today

app = Flask(__name__)

@app.route('/')
def hello():
    file_name = get_filename_for_today()
    file_data = get_or_generate_file(file_name, create_default_daily_tasks_object)
    return render_template('todo.html', data=file_data)

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

        file_name = get_filename_for_today()

        # Read the existing data from the JSON file
        existing_data = get_or_generate_file(file_name, create_default_daily_tasks_object)

        existing_data[field_name] = new_value

        # Save the updated data back to the JSON file
        write_file(file_name, existing_data)

        return jsonify({"message": "Field updated successfully."}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

def authenticate_request(data):
    return data.get('password') == "temp"

if __name__ == '__main__':
    app.run()
