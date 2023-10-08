from datetime import datetime, timedelta
import pytz

def get_filename_for_today():
    pacific_timezone = pytz.timezone('US/Pacific')

    current_datetime = datetime.now(pacific_timezone)

    # Check if the current time is before 2 am PST
    if current_datetime.hour < 2:
        # If before 2 am, use yesterday's date
        current_datetime -= timedelta(days=1)

    filename = f"todo_list_{current_datetime.strftime('%Y-%m-%d')}.json"
    return filename